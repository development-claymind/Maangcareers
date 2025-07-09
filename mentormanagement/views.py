from django.shortcuts import render

# Create your views here.
from .models import BatchCompleteRequest
from .models import *
from rest_framework.generics import ListAPIView , RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated
from knox.auth import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from courseManagement.models import *
from testsManagement.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import random
import ast
from datetime import datetime ,timedelta
from django.db.models import Max
import time
import requests
import json
from rest_framework import serializers
from collections import defaultdict
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.hashers import make_password


def get_completed_days(timetable):
    current_datetime = datetime.now()
    completed_days = []
    for index, entry in enumerate(timetable):
        start_date = entry.get('start_date')
        start_time = entry.get('start_time')
        start_datetime = datetime.combine(start_date, start_time) if start_date and start_time else None

        if start_datetime and current_datetime >= start_datetime:
            completed_days.append(index + 1)
    return completed_days

def current_batch(timetable):
    max_date = None

    for entry in timetable:
        start_date = entry.get('start_date')
        if start_date:
            if max_date is None or start_date > max_date :
                max_date = start_date
                

    max_date = max_date + timedelta(30)
    current_date = datetime.now().date()
    if max_date > current_date:
        return True
    else:
        return False

class InstructorTermsAndConditionView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user_id = request.user.id      
        inst_obj = Instructor.objects.get(user_id=user_id)
        message = 1 if inst_obj.terms_condition else 0
        return Response({"message":message}, status=status.HTTP_200_OK)
    def post(self, request):
        user_id = request.user.id      
        inst_obj = Instructor.objects.get(user_id=user_id)
        terms_conditions = request.data.get('terms_conditions', False)
        if not inst_obj.terms_condition:
            inst_obj.terms_condition = terms_conditions
            inst_obj.save()
            return Response({"message":1}, status=status.HTTP_200_OK)
        else:
            return Response({"message":0}, status=status.HTTP_400_BAD_REQUEST)

class InstructorRulesAndRegulationView(ListAPIView):

    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user_id = request.user.id      
        inst_obj = Instructor.objects.get(user_id=user_id)
        counter = 1 if inst_obj.rules_regulation_count  else 0
        return Response({"counter":counter}, status=status.HTTP_200_OK)
    def post(self, request):
        user_id = request.user.id      
        inst_obj = Instructor.objects.get(user_id=user_id)
        count = int(request.data.get('count'))
        if count == 10 :
            inst_obj.rules_regulation_count = 1
            inst_obj.save()
            return Response({'message': 'Count updated successfully'})
        else:
            return Response({'message': 'complete all steps'})
        
class InstructorProfileUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )

class InstructorProfileSerializer(ModelSerializer):
    user = InstructorProfileUserSerializer()
    class Meta:
        model = Instructor
        fields = (
            'phone_num',
            'user'
        )

class InstructorProfileViewSet(RetrieveAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    queryset = Instructor.objects.all()
    serializer_class = InstructorProfileSerializer
    
class InstructorProfilePasswordUpdate(RetrieveAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    queryset = Instructor.objects.all()
    serializer_class = InstructorProfileSerializer
    def post(self, request):
        try:
            user_id = request.user.id
            obj_user = User.objects.get(id=user_id)
            old_password = request.POST.get("old_password")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if len(old_password) != 0 and len(password1) != 0 and len(password2) != 0 and password1 != None and password2 != None and password1 == password2:
                if obj_user.check_password(old_password) :
                    password = make_password(password1)
                    obj_user.password = password
                    obj_user.save()
                    return Response({"message":1}, status=status.HTTP_200_OK)
                else:
                    return Response({"message":0}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":0}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e :
            return Response({"error":f"{e}"})

class InstructorProfileInfo(RetrieveAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    queryset = Instructor.objects.all()
    serializer_class = InstructorProfileSerializer

    def get(self, request):
        try:
            user_id = request.user.id      
            inst_obj = Instructor.objects.get(user_id=user_id)
            ph = inst_obj.phone_num
            profile_pic = inst_obj.photo.url if inst_obj.photo else None
            f_nm = inst_obj.user.first_name
            l_nm = inst_obj.user.last_name
            email = inst_obj.user.email
            get_batch = Batch.objects.filter(instructor__id=inst_obj.id)
            data = []
            if get_batch.exists():
                for i in get_batch:
                    batch_info = {
                        'batch_id':i.id,
                        'course': i.course.name,
                        'start_date': i.start_date,
                        'end_date': i.end_date,
                    }
                    data.append(batch_info)
                return Response({"message":1,"Instructor_f_nm":f_nm,"Instructor_l_nm":l_nm,"Instructor_email":email,"Instructor_ph_no":ph,"Instructor_profile_pic":profile_pic,"Inst_course_details":data}, status=status.HTTP_200_OK)
            else:
                return Response({"message":0}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e :
            return Response({"error":f"{e}"})   
        
class InstructorProfileDetailsUpdate(RetrieveAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    queryset = Instructor.objects.all()
    serializer_class = InstructorProfileSerializer

    def post(self, request):
        try:
            user_id = request.user.id      
            obj_user = User.objects.get(id=user_id)
            inst_obj = Instructor.objects.get(user_id=user_id)
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            profile_pic = request.FILES.get("profile_pic")
            if len(first_name) != 0 and len(last_name) != 0  and first_name != None and last_name != None :
                obj_user.first_name = first_name 
                obj_user.last_name  = last_name
                obj_user.save() 
                inst_obj.photo = profile_pic
                inst_obj.save() 
                return Response({"message":1}, status=status.HTTP_200_OK)
            else:
                return Response({"message":0}, status=status.HTTP_400_BAD_REQUEST)        
        except Exception as e :
            return Response({"error":f"{e}"})        

class InstructorDashboardCalenderViewList(ListAPIView):  #19/01/2024
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try :
            user_id = request.user.id
            inst_id = [i["id"] for i in Instructor.objects.filter(user_id=user_id).values("id")]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
            get_batch = Batch.objects.filter(instructor_id__in=inst_id).values("id", "course_id")
            batch_ids = [i["id"] for i in get_batch]
            course_ids = list(set(i["course_id"] for i in get_batch))
            all_times = TimeTable.objects.filter(batch__course_id__in=course_ids, batch_id__in=batch_ids).values(
                    "batch_id","batch__course__name", "start_date", "week"
                ).order_by("batch__course__name", "week", "start_date")
            result_data = {}
            for entry in all_times:
                date_key = entry["start_date"]
                course_name = entry["batch__course__name"]
                if date_key in result_data:
                    result_data[date_key]["course_names"].append(course_name)
                else:
                    result_data[date_key] = {
                        # "batch_id": entry["batch_id"],
                        "date": entry["start_date"],
                        "course_names": [course_name],
                        "week": entry["week"],
                    }
            result_list = list(result_data.values())
            return Response({"message": 1, "all_data": result_list}, status=status.HTTP_200_OK)
        except:
            return Response({"message": 0}, status=status.HTTP_400_BAD_REQUEST)          
        
class InstructorClassCompleteProgressBar(ListAPIView):  #19/01/2024
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            user_id = request.user.id
            inst_id = [i["id"] for i in Instructor.objects.filter(user_id=user_id).values("id")]

            get_batch = Batch.objects.filter(instructor_id__in=inst_id).values("id", "course_id")
            course_ids = list(set(i["course_id"] for i in get_batch))
            get_batches = Batch.objects.filter(instructor_id__in=inst_id, course_id__in=course_ids , completed = False ).values("id", "course__name", "start_date", "end_date")

            if not get_batches.exists():
                return Response({"course_info": "Course not found", "message": 0}, status=status.HTTP_200_OK)

            batch_details = []
            for batch_info in get_batches:
                batch_info = {
                    "batch_id": batch_info["id"],
                    "course_name": batch_info["course__name"],
                    "start_date": batch_info["start_date"],
                    "end_date": batch_info["end_date"],
                }
                batch_details.append(batch_info)

            course_attendance = defaultdict(lambda: {"total_cls_sum": 0, "completed_classes_sum": 0})
            batch_details_user = list(Batch.objects.filter(instructor_id__in=inst_id, completed=False).values_list("id", flat=True))
            current_batch_list = []

            for i in batch_details_user:
                time_table = TimeTable.objects.filter(batch_id=i).values("start_date", "start_time")
                current_batch_ = current_batch(time_table)
                if current_batch_:
                    current_batch_list.append(i)

            if len(current_batch_list) == 0:  
                return Response({"status": "Batch not found"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                response_data = [] 

                for batch_info in batch_details:
                    batch_id = batch_info["batch_id"]
                    time_table = TimeTable.objects.filter(batch_id=batch_id).values("start_date", "start_time")
                    total_cls = len(time_table)
                    completed_classes = get_completed_days(list(time_table))
                    course_name = batch_info["course_name"]
                    start_date = batch_info["start_date"]
                    end_date = batch_info["end_date"]
                    course_attendance[course_name]["total_cls_sum"] += total_cls
                    course_attendance[course_name]["completed_classes_sum"] += len(completed_classes)
                    total_cls_sum = total_cls
                    completed_classes_sum = len(completed_classes)
                    remaining_classes = total_cls_sum - completed_classes_sum
                    cls_attend_percentage = (completed_classes_sum / total_cls_sum) * 100 if total_cls_sum > 0 else 0
        
                    if remaining_classes != 0:
                        response_data.append({
                            "batch_id": batch_id,
                            "course_name": course_name,
                            "start_date": start_date,
                            "end_date": end_date,
                            "total_class": total_cls_sum,
                            "num_of_completed_classes": completed_classes_sum,
                            "remaining_classes": remaining_classes,
                            "cls_percentage": f"{cls_attend_percentage:.2f}",
                            "status": "",
                        })
                    else:
                        response_data.append({
                            "batch_id": batch_id,
                            "course_name": course_name,
                            "start_date": start_date,
                            "end_date": end_date,
                            "total_class": total_cls_sum,
                            "num_of_completed_classes": completed_classes_sum,
                            "remaining_classes": remaining_classes,
                            "cls_percentage": f"{cls_attend_percentage:.2f}",
                            "status": "Classes completed !",
                        })

                return Response({"coursewise_progress": response_data, "message": 1}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)         

class InstructorTimetableViewList(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            user_id = request.user.id
            inst_id = [i["id"] for i in Instructor.objects.filter(user_id=user_id).values("id")]
            get_batch = Batch.objects.filter(instructor_id__in=inst_id).values("id", "course_id")
            batch_ids = [i["id"] for i in get_batch]
            course_ids = [i["course_id"] for i in get_batch]
            all_times_week = TimeTable.objects.filter(
                batch__course_id__in=course_ids,
                batch_id__in=batch_ids 
            ).values(
                "id",
                "batch_id",
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
                    "batch_id":entry["batch_id"],
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
        
class InstructorDashboardOngoingUpcomingUpdates(ListAPIView):  
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)        
    def get(self, request): 
        try:
            user_id = request.user.id
            inst_id = [i["id"] for i in Instructor.objects.filter(user_id=user_id).values("id")]
            get_batch = Batch.objects.filter(instructor_id__in=inst_id).values("id", "course_id")
            # course_ids = [i["batch__course_id"] for i in get_batch]
            batch_ids = [i["id"] for i in get_batch]
            all_timetable = []
            for i in batch_ids:
                timetable = list(TimeTable.objects.filter(batch_id=i).values("id", "start_date", "start_time", "end_time", "link", "week", "batch_id", "day"))
                all_timetable += timetable
            sorted_all_timetable = sorted(all_timetable, key=lambda x: (x['start_date'], x['start_time']))
            current_datetime = datetime.now()
            past_classes = [c for c in sorted_all_timetable if c['end_time'] and datetime.combine(c['start_date'], c['end_time']) < current_datetime]
            future_classes = [c for c in sorted_all_timetable if c['end_time'] and datetime.combine(c['start_date'], c['end_time']) >= current_datetime]
            for post_class in past_classes:
                post_class["course"] = Batch.objects.filter(id=post_class["batch_id"]).values("course__name")[0]["course__name"]
                post_class["time_table_topic"] = TimeTable.objects.filter(week=post_class["week"], day=post_class["day"], batch_id = post_class["batch_id"]).values("topic")[0]["topic"]
                week_id = list(Week.objects.filter(week=post_class["week"], course_id=int(Batch.objects.filter(id=post_class["batch_id"]).values("course_id")[0]["course_id"])).values("id"))
                today_topic_list = Topic.objects.filter(week_id=int(week_id[0]["id"]), day=post_class["day"]).values("name")
                if len(today_topic_list) == 0:
                    post_class["today_topic"] = ""
                else:
                    post_class["today_topic"] = today_topic_list[0]["name"]
            ongoing_data = []
            upcoming_data = []
            all_upcoming_data = []
            if len(future_classes) == 1:
                data = future_classes[0]
                data["course"] = Batch.objects.filter(id=data["batch_id"]).values("course__name")[0]["course__name"]
                data["time_table_topic"] = TimeTable.objects.filter(week=data["week"], day=data["day"], batch_id = data["batch_id"]).values("topic")[0]["topic"]
                week_id = list(Week.objects.filter(week=data["week"], course_id=int(Batch.objects.filter(id=data["batch_id"]).values("course_id")[0]["course_id"])).values("id"))
                today_topic_list = Topic.objects.filter(week_id=int(week_id[0]["id"]), day=data["day"]).values("name")
                if len(today_topic_list) == 0:
                    data["today_topic"] = ""
                else:
                    data["today_topic"] = today_topic_list[0]["name"]
                ongoing_data.append(data)
                data = {"message": "No Upcoming Class"}
                upcoming_data.append(data)
            elif len(future_classes) > 1:
                data = future_classes[0]
                data["course"] = Batch.objects.filter(id=data["batch_id"]).values("course__name")[0]["course__name"]
                data["time_table_topic"] = TimeTable.objects.filter(week=data["week"], day=data["day"], batch_id = data["batch_id"]).values("topic")[0]["topic"]
                week_id = list(Week.objects.filter(week=data["week"], course_id=int(Batch.objects.filter(id=data["batch_id"]).values("course_id")[0]["course_id"])).values("id"))
                today_topic_list = Topic.objects.filter(week_id=int(week_id[0]["id"]), day=data["day"]).values("name")
                if len(today_topic_list) == 0:
                    data["today_topic"] = ""
                else:
                    data["today_topic"] = today_topic_list[0]["name"]
                ongoing_data.append(data)
                data = future_classes[1]
                data["course"] = Batch.objects.filter(id=data["batch_id"]).values("course__name")[0]["course__name"]
                data["time_table_topic"] = TimeTable.objects.filter(week=data["week"], day=data["day"], batch_id = data["batch_id"]).values("topic")[0]["topic"]
                week_id = list(Week.objects.filter(week=data["week"], course_id=int(Batch.objects.filter(id=data["batch_id"]).values("course_id")[0]["course_id"])).values("id"))
                today_topic_list = Topic.objects.filter(week_id=int(week_id[0]["id"]), day=data["day"]).values("name")
                if len(today_topic_list) == 0:
                    data["today_topic"] = ""
                else:
                    data["today_topic"] = today_topic_list[0]["name"]
                upcoming_data.append(data)
            else:
                pass
            for data in future_classes:
                data["course"] = Batch.objects.filter(id=data["batch_id"]).values("course__name")[0]["course__name"]
                data["time_table_topic"] = TimeTable.objects.filter(week=data["week"], day=data["day"], batch_id=data["batch_id"]).values("topic")[0]["topic"]
                week_id = list(Week.objects.filter(week=data["week"], course_id=int(Batch.objects.filter(id=data["batch_id"]).values("course_id")[0]["course_id"])).values("id"))
                today_topic_list = Topic.objects.filter(week_id=int(week_id[0]["id"]), day=data["day"]).values("name")
                if len(today_topic_list) == 0:
                    data["today_topic"] = ""
                else:
                    data["today_topic"] = today_topic_list[0]["name"]
                all_upcoming_data.append(data)  

            data = {"ongoing": ongoing_data, "upcoming": upcoming_data, "all_upcoming_data": all_upcoming_data, "recent_passed": past_classes[::-1]}
            return Response({"response_data": data}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"error":f"{e}"})        
        
class InstructorCourseSelection(ListAPIView):   #24/01/2024
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            user_id = request.user.id
            inst_obj = Instructor.objects.get(user_id=user_id)   
            data =[]
            course_batches_details = Batch.objects.filter(instructor_id = inst_obj.id ,completed = False).values("id" ,"course_id" ,"course__name")
            if course_batches_details.exists():
                for i in course_batches_details:
                        batch_info = {
                            'batch_id':i["id"],
                            'course_id': i["course_id"],
                            'course__name': i["course__name"], 
                        }
                        data.append(batch_info)
                return Response({"message":1,"course_batches_details":data}, status=status.HTTP_200_OK)
            else:
                data =[]
                return Response({"message":0,"course_batches_details":data}, status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e :
            return Response({"error":f"{e}"})        

class InstructorOngoingPreviousBatchSelection(ListAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            user_id = request.user.id
            course_id = request.GET.get('course_id')  
            inst_obj = Instructor.objects.get(user_id=user_id)   
            ongoing_batches = Batch.objects.filter(instructor_id = inst_obj.id ,course_id = course_id, completed = False)
            previous_batches = Batch.objects.filter(instructor_id = inst_obj.id ,course_id = course_id, completed = True)
            
            data = {
                "ongoing_batches_ids": list(ongoing_batches.values("id")) if ongoing_batches.exists() else None,
                "previous_batches_ids": list(previous_batches.values("id")) if previous_batches.exists() else None,
            }
            return Response({"message": 1, "data": data}, status=status.HTTP_200_OK)   
        except Exception as e :
            return Response({"error":f"{e}"})           

################################### Mentor Teaching Section ################################################
    
def prc_week_first_questions(course_id, week_id):
    get_q = CompilerQuestion.objects.filter(week=week_id,course_id=course_id,practice_mock=False).order_by("day").first()
    
    if get_q:
        topics = {"q_id":get_q.id,"title":get_q.ques_title,"slg":get_q.ques_title.replace(" ", "-")}
    else:
        topics = {"q_id":None,"title":None,"slg":None}
    return topics

class InstructorAllNotesWeekLock(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            user_id = request.user.id
            course_id = request.GET.get("course_id")
            inst_id = [i["id"] for i in Instructor.objects.filter(user_id=user_id).values("id")]
            get_batch = Batch.objects.filter(instructor_id__in=inst_id).values("id", "course_id")
            batch_ids = [i["id"] for i in get_batch]
            all_times = TimeTable.objects.filter(batch__course_id=course_id,batch_id__in=batch_ids).values("week","start_date","start_time","batch__course__name").order_by("id")
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d-%H:%M:%S")
            week_conut = []
            for i in all_times :
                if f"{i['start_date']}-{i['start_time']}" < formatted_datetime :
                    week_conut.append(i["week"])
            main_data = []
            for i in range(1,9) :
                if  week_conut.count(str(i)) >= 1 :
                    std_all_note = Note.objects.filter(course_id=course_id,week=i) 
                    if std_all_note.exists():
                        std_all_note = std_all_note.first()
                        file = f"{std_all_note.file.url}"
                        main_data.append({"topic":std_all_note.topic,"week":i,"file":file,"week_status":"unlock","condition":""})
                    else:
                        main_data.append({"topic":"","week":i,"file":"","week_status":"unlock","condition":"no notes at this moment"})
                else:
                    main_data.append({"topic":"","week":i,"file":"","week_status":"lock"})
            return Response({"main_data":main_data})
        except Exception as e :
            return Response({"error":f"{e}"})       

class InstructorTeachingPracticeWeekLock(ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try :
            user_id = request.user.id
            course_id = request.GET.get("course_id")
            inst_id = [i["id"] for i in Instructor.objects.filter(user_id=user_id).values("id")]
            get_batch = Batch.objects.filter(instructor_id__in=inst_id).values("id", "course_id")
            batch_ids = [i["id"] for i in get_batch]
            if not course_id :
                course_ids = [i["course_id"] for i in get_batch]
                queryset = Course.objects.filter(id__in=course_ids).values("id","name").order_by("name")
                course_id = queryset.first()["id"]
                course_name = queryset.first()["name"]
            else:
                queryset = Course.objects.filter(id=course_id).values("id","name")
                course_id = queryset.first()["id"]
                course_name = queryset.first()["name"]

            all_times = TimeTable.objects.filter(batch__course_id=course_id,batch_id__in=batch_ids).values("week","start_date","start_time","batch__course__name").order_by("id")
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d-%H:%M:%S")
            week_conut = []
            for i in all_times :
                if f"{i['start_date']}-{i['start_time']}" < formatted_datetime :
                    week_conut.append(i["week"])
            main_data = []
            result = []
            
            
            for i in range(1,9) :
                total_question = CompilerQuestion.objects.filter(practice_mock=False,week=str(i))
                complted_question = 0
                pre_week_complted_question = 0
                pre_week_total_question = CompilerQuestion.objects.filter(practice_mock=False,week=str(i-1))
                for k in total_question.values("id"):
                    check_com = CompilerQuestionAtempt.objects.filter(student_id = inst_id[0], button_clicked = 'Submit', question__week = str(i), question__practice_mock=False, status=True,  question_id=int(k["id"])).values("id").count()
                    if check_com >= 1:
                        complted_question = complted_question + 1
                for l in pre_week_total_question.values("id"):
                    check__com = CompilerQuestionAtempt.objects.filter(student_id = inst_id[0], button_clicked = 'Submit', question__week = str(i-1), question__practice_mock=False, status=True,  question_id=int(k["id"])).values("id").count()
                    if check__com >= 1:
                        pre_week_complted_question = pre_week_complted_question + 1
                if  week_conut.count(str(i)) >= 1:
                    if i == 1:
                        if len(total_question) != 0:
                            main_data.append({
                                "week": i,
                                "name": course_name,
                                "img": "/images/Practice/week2.svg",
                                "status": True,
                                "completed": complted_question,
                                "total": len(total_question),
                                "isDisabled": False,
                                "condition":""
                                })
                        else:
                            main_data.append({
                                "week": i,
                                "name": course_name,
                                "img": "/images/Practice/week2.svg",
                                "status": True,
                                "completed": complted_question,
                                "total": len(total_question),
                                "isDisabled": False,
                                "condition":"Reach out to support team to unlock this"
                                })
                    else:
                        if len(total_question) != 0:
                            
                            main_data.append({
                                "week": i,
                                "name": course_name,
                                "img": "/images/Practice/week2.svg",
                                "status": True,
                                "completed": complted_question,
                                "total": len(total_question),
                                "isDisabled": False,
                                "condition":""
                                })
                        else:
                            main_data.append({
                                "week": i,
                                "name": course_name,
                                "img": "/images/Practice/week2.svg",
                                "status": True,
                                "completed": complted_question,
                                "total": len(total_question),
                                "isDisabled": False,
                                "condition":"Reach out to support team to unlock this"
                                })
                else:
                    main_data.append({
                        "week": i,
                        "name": course_name,
                        "img": "/images/Practice/week2.svg",
                        "status": False,
                        "completed": complted_question,
                        "total": len(total_question),
                        "isDisabled": True,
                        })
            for i in range(1, len(main_data)+1):
                prc_week_first = prc_week_first_questions(course_id, str(i))
                week_data = main_data[i-1]
                week_data.update(prc_week_first)
                result.append(week_data)
            return Response({"main_data":result})
        except Exception as e :
            return Response({"error":f"{e}"})     




