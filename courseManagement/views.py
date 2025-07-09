# from django.shortcuts import render
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView
from knox.auth import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Course, Week, TimeTable, Batch, Note ,BatchJoined
from testsManagement.models import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import date 
from django.db.models import F
from django.shortcuts import redirect

class WeekSerializer(ModelSerializer):
    class Meta:
        model = Week
        fields = (
            "name",
            # "course",
            "lock",
            "lessons"
        )
        depth=1
class CourseSerializer(ModelSerializer):
    syllabi = WeekSerializer(many=True)
    class Meta:
        model = Course
        fields = (
            "author_message",
            "author_name",
            "author_photo",
            "caption",
            "certificate",
            "class_duration",
            "course_duration",
            "demo_video",
            "description",
            "discount_percentage",
            "id",
            "lectures",
            "mobile_computer",
            "name",
            "popular",
            "pre_recorded",
            "premium",
            "price",
            "projects",
            "requirements",
            "short_description",
            "thumbnail",
            "payment_id",
            "syllabi",
        )
class CourseListSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = (
            "course_duration",
            "discount_percentage",
            "id",
            "lectures",
            "name",
            "popular",
            "premium",
            "price",
            "projects",
            "short_description",
            "thumbnail",
            "payment_id"
        )

class CourseViewSet(ViewSet):
    """
    A simple ViewSet for listing Courses.
    """
    def list(self, request):
        queryset = Course.objects.filter(archive=False)
        serializer = CourseListSerializer(queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        queryset = Course.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(user)
        return Response(serializer.data)
    
class TimeTableSerializer(ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'
class TimeTableViewSet(ListAPIView):
    queryset = TimeTable.objects.filter(Q(start_date__lte=date.today()))
    serializer_class = TimeTableSerializer

class UserCourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id','name')
class UserBatchSerializer(ModelSerializer):
    timetable = TimeTableSerializer(many=True)
    course = UserCourseSerializer()
    class Meta:
        model = Batch
        fields = (
            'id',
            'name',
            'course',
            'start_date',
            'end_date',
            # 'instructor',
            'timetable'
        )
        depth = 1
class UserBatchViewSet(ListAPIView):
    queryset = Batch.objects.all()
    serializer_class = UserBatchSerializer

    def get(self, request, *args, **kwargs):
        batches = self.request.user.student.batches.all()
        self.queryset = batches.filter(Q(end_date=None) | Q(end_date__gte=date.today()))
        return super().get(request, *args, **kwargs)
    
class PaymentViewSet(ViewSet):

    def create(self, request):
        course_id = request.data['course_id']
        batch = Course.objects.get(id=course_id).batches.filter(start_date__gte=date.today()).order_by('start_date')
        for b in batch:
            if b.students.count() < b.max_participants:
                batch = b
                break
        else:batch = Batch.objects.create(course = Course.objects.get(id=course_id))
        # if not batch or batch.students.count() >= batch.max_participants:batch = Batch.objects.create(course = Course.objects.get(id=course_id))
        batch.students.add(request.user.student)
        batch.joined.filter(student=request.user.student).update(payment_id=request.data['payment_id'])
        return Response({'message':'Payment Successful'})
        
class NoteListSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = (
            "topic",
            # "course",
            "week",
            "file"
        )
class NoteViewSet(ListAPIView):
    """
    A simple ViewSet for listing Notes.
    """
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication,]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course',]
    queryset = Note.objects.all()
    serializer_class = NoteListSerializer
    pagination_class = None

class CertificateListSerializer(ModelSerializer):
    course_name = SerializerMethodField()
    class Meta:
        model = Batch
        fields = (
            "id",
            "course_name",
            "start_date",
            "end_date",
        )
    def get_course_name(self,obj) -> str:return obj.course.name

class CertificateViewSet(ListAPIView):
    """
    A simple ViewSet for listing Certificates.
    """

    authentication_classes = [TokenAuthentication,]
    serializer_class = CertificateListSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = self.request.user.student.batches.filter(completed=True)
        return queryset

#29/12/2023
class StudentClassTimeTableViewSet(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
   
    def get(self, request):
        try:
            user_id = request.user.id
            std_id = [i["id"] for i in Student.objects.filter(user_id=user_id).values("id")]
            get_batch = BatchJoined.objects.filter(student_id__in=std_id).values("batch_id", "batch__course_id")
            batch_ids = [i["batch_id"] for i in get_batch]
            course_ids = [i["batch__course_id"] for i in get_batch]
            all_times = TimeTable.objects.filter(batch__course_id__in=course_ids, batch_id__in=batch_ids).values(
                "batch__course__name", "start_date", "week"
            ).order_by("batch__course__name", "week", "start_date")
            result_data = {}
            for entry in all_times:
                date_key = entry["start_date"]
                course_name = entry["batch__course__name"]
                if date_key in result_data:
                    result_data[date_key]["course_names"].append(course_name)
                else:
                    result_data[date_key] = {
                        "date": entry["start_date"],
                        "course_names": [course_name],
                        "week": entry["week"],
                    }
            result_list = list(result_data.values())
            return Response({"message": 1, "all_data": result_list}, status=status.HTTP_200_OK)
        except:
            return Response({"message": 0}, status=status.HTTP_400_BAD_REQUEST)

#05/01/2024      
class StudentClassesRoutineViewSet(ListAPIView): # code update
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_id = request.user.id
            std_id = [i["id"] for i in Student.objects.filter(user_id=user_id).values("id")]
            get_batch = BatchJoined.objects.filter(student_id__in=std_id).values("batch_id", "batch__course_id")
            batch_ids = [i["batch_id"] for i in get_batch]
            course_ids = [i["batch__course_id"] for i in get_batch]
            all_times_week = TimeTable.objects.filter(
                batch__course_id__in=course_ids,
                batch_id__in=batch_ids 
            ).values(
                "id",
                "batch__course__name",
                "batch__course__id",
                "topic",
                "start_date",
                "start_time",
                "week",
                "day",
                "link"
            ).order_by("week", "start_date", F("start_time"),F("week").asc(nulls_last=True))

            if not all_times_week:
                return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
            grouped_data = {}
            for entry in all_times_week:
                date = entry["start_date"]
                if date not in grouped_data:
                    grouped_data[date] = []
                day_topic_list =Topic.objects.filter(week__course = entry["batch__course__id"],week__week=entry["week"],day = entry["day"]).values("name")
                if len(day_topic_list) != 0:
                    day_topic = day_topic_list[0]["name"]
                else:
                    day_topic = None
                entry_info = {
                    "id":entry["id"],
                    "batch__course__name": entry["batch__course__name"],
                    "topic": entry["topic"],
                    "start_time": entry["start_time"],
                    "week": entry["week"],
                    "day": entry["day"],
                    "day_topic": day_topic,
                    "link": entry["link"],
                }
                grouped_data[date].append(entry_info)
            # Sort courses within each date by start_time
            for courses in grouped_data.values():
                courses.sort(key=lambda x: x["start_time"])
            result = [{"date": date, "courses": courses} for date, courses in grouped_data.items()]
            return Response({"message": 1, "week_data": result}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error":f"{e}"}) 

#05/01/2024
# class StudentProjectAssign(ListAPIView):
#     def get(self, request, b_id):
#         try:
#             batch_id = b_id
#             get_batch_join = list(BatchJoined.objects.filter(batch__id=batch_id).values("id","batch_id","batch__course__name","assign_topic","assign_project"))
#             get_batch = Batch.objects.filter(id=batch_id ).values( "id","course_id","course__name","project_topic__project_topic", "project_topic","project_topic__project_name")
#             project_names_lst = list(set(i["project_topic__project_name"] for i in get_batch))
#             pro_topic = get_batch[0]["project_topic"]
#             output = []
#             for i in range(len(get_batch_join)):
#                 get_batch_join[i]["assign_project"] = project_names_lst[i % len(project_names_lst)]
#                 get_batch_join[i]["assign_topic"] = pro_topic
#                 output.append(get_batch_join[i])
#             for k in output:
#                 BatchJoined.objects.filter(id=k["id"]).update(assign_topic_id=k["assign_topic"], assign_project_id=k["assign_project"])
            
#             return Response({"ststus":1}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)
        
#10/01/2024
class StudentProjectAssign(ListAPIView):
    def get_queryset(self):
        return BatchJoined.objects.all()
    def get(self, request, b_id):
        try:
            batch_id = b_id
            get_batch_join = list(BatchJoined.objects.filter(batch__id=batch_id).values("id","batch_id","batch__course__name","assign_topic","assign_project"))
            get_batch = Batch.objects.filter(id=batch_id).values( "id","course_id","course__name","project_topic__project_topic", "project_topic","project_topic__project_name")
            project_names_lst = list(set(i["project_topic__project_name"] for i in get_batch))
            pro_topic = get_batch[0]["project_topic"]
            output = []
            for i in range(len(get_batch_join)):
                get_batch_join[i]["assign_project"] = project_names_lst[i % len(project_names_lst)]
                get_batch_join[i]["assign_topic"] = pro_topic
                output.append(get_batch_join[i])
            for k in output:
                BatchJoined.objects.filter(id=k["id"]).update(assign_topic_id=k["assign_topic"], assign_project_id=k["assign_project"])
            return redirect('../../admin/courseManagement/batch/')       
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)                