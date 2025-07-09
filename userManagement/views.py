# from django.shortcuts import render

# from .models import Notice, Student
from .models import *
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.serializers import ModelSerializer
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from courseManagement.models import *
from testsManagement.models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



class NoticeSerializer(ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

class NoticeViewSet(ListAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

class ProfileUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )

class ProfileSerializer(ModelSerializer):
    user = ProfileUserSerializer()
    class Meta:
        model = Student
        fields = (
            'phone_num',
            'user'
        )

class ProfileViewSet(RetrieveAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = ProfileSerializer

class ProfilePasswordUpdate(RetrieveAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = ProfileSerializer
    def post(self, request):
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
        
# class StudentProfileInfo(RetrieveAPIView):
#     authentication_classes = [TokenAuthentication,]
#     permission_classes = (IsAuthenticated,)
#     queryset = Student.objects.all()
#     serializer_class = ProfileSerializer

#     def get(self, request):
#         user_id = request.user.id      
#         std_obj = Student.objects.get(user_id=user_id)
#         ph = std_obj.phone_num
#         profile_pic = std_obj.profile_img.url if std_obj.profile_img else None
#         f_nm = std_obj.user.first_name
#         l_nm = std_obj.user.last_name
#         email = std_obj.user.email
#         get_batch = BatchJoined.objects.filter(student__id=std_obj.id)
#         data = []
#         if get_batch.exists():
#             for i in get_batch:
#                 batch_info = {
#                     'course': i.batch.course.name,
#                     'start_date': i.batch.start_date,
#                     'end_date': i.batch.end_date,
#                 }
#                 data.append(batch_info)
#             return Response({"message":1,"Student_f_nm":f_nm,"Student_l_nm":l_nm,"Student_email":email,"Student_ph_no":ph,"Student_profile_pic":profile_pic,"Stud_course_details":data}, status=status.HTTP_200_OK)
            
#         else:
#             return Response({"message":0}, status=status.HTTP_400_BAD_REQUEST)

#05/01/2024        
class StudentProfileInfo(RetrieveAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request):
        try:
            user_id = request.user.id      
            std_obj = Student.objects.get(user_id=user_id)
            ph = std_obj.phone_num
            terms_conditions = std_obj.terms_condition
            profile_pic = std_obj.profile_img.url if std_obj.profile_img else None
            f_nm = std_obj.user.first_name
            l_nm = std_obj.user.last_name
            email = std_obj.user.email
            get_batch = BatchJoined.objects.filter(student__id=std_obj.id)
            batch_join = BatchJoined.objects.filter(student__id=std_obj.id).values("assign_topic__project_topic", "assign_project__project_name", "batch__course__name")
            project_data = [
                {"project_title": i["assign_topic__project_topic"], "project_topic": i["assign_project__project_name"], "course": i["batch__course__name"]}
                for i in batch_join
            ]
            data = []
            if get_batch.exists():
                for i in get_batch:
                    batch_info = {
                        'course': i.batch.course.name,
                        'start_date': i.batch.start_date,
                        'end_date': i.batch.end_date,
                        'stud_project_assign': [
                            {"project_title": project["project_title"], "project_topic": project["project_topic"]}
                            for project in project_data if project["course"] == i.batch.course.name
                        ]
                    }
                    data.append(batch_info)

                return Response({"message": 1, "Student_f_nm": f_nm, "Student_l_nm": l_nm, "Student_email": email, "Student_ph_no": ph, "Student_terms_conditions": terms_conditions, "Student_profile_pic": profile_pic, "Stud_course_details": data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": 0}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": e}, status=status.HTTP_400_BAD_REQUEST)        
        
class ProfileDetailsUpdate(RetrieveAPIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = ProfileSerializer

    def post(self, request):
        user_id = request.user.id      
        obj_user = User.objects.get(id=user_id)
        std_obj = Student.objects.get(user_id=user_id)
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        profile_pic = request.FILES.get("profile_pic")
        if len(first_name) != 0 and len(last_name) != 0  and first_name != None and last_name != None :
            obj_user.first_name = first_name 
            obj_user.last_name  = last_name
            obj_user.save() 
            std_obj.profile_img = profile_pic
            std_obj.save() 
            return Response({"message":1}, status=status.HTTP_200_OK)
        else:
            return Response({"message":0}, status=status.HTTP_400_BAD_REQUEST)

#new_change1      
class AllNotifications(ListAPIView):  # new code
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try :
            all_notice = Notice.objects.all().order_by("-id")
            std_id = [i["id"] for i in Student.objects.filter(user_id=request.user.id).values("id")]
            stud_notification = NotificationStatus.objects.filter(student_id=std_id[0])
            data = []
            notice_count = 0
            if stud_notification.exists():
                previous_notification = stud_notification.values("notice__id")
                previous_notification_id = [i["notice__id"] for i in previous_notification]
                all_notice = all_notice.exclude(id__in=previous_notification_id)
            else:
                pass
            msg_details = MessageDetails.objects.filter(student_id = std_id[0], is_read=False)
            for j in msg_details:
                notice_info = {
                    'notice_id': j.id,
                    'condition':j.title,
                    'status': "autometic notice",
                    'content': j.content,
                    'date': j.message_created,
                }
                data.append(notice_info)

            for i in all_notice :
                notice_info = {
                    'notice_id': i.id,
                    'status': "manual notice",
                    'content': i.content,
                    'date': i.date,
                }
                data.append(notice_info)
            notice_count = len(data)
            return Response({"message":1 ,"notification_count":notice_count,"current_notification":data}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"message":0,"error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

#new_change1     
class MarkAsRead(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            notification_id = request.POST.get('notification_id')
            status_msg = request.POST.get('status_msg')
            std_id = [i["id"] for i in Student.objects.filter(user_id=request.user.id).values("id")]
            if status_msg == 'manual notice' :
                stud_notification = NotificationStatus.objects.filter(student_id__in=std_id)
                all_notice = Notice.objects.all().order_by("-id").values("id")
                if stud_notification.exists():
                    previous_notification = stud_notification.values("notice__id")
                    previous_notification_id = [i["notice__id"] for i in previous_notification]
                    all_notice = all_notice.exclude(id__in=previous_notification_id)
                    stud_notification = stud_notification.first()
                    save_n = NotificationStatus.objects.get(id=stud_notification.id)
                    save_n.notice.add(notification_id)
                else:
                    save_notification = NotificationStatus(student_id=std_id[0])
                    save_notification.save()
                    save_notification.notice.add(notification_id)
            else:
                MessageDetails.objects.filter(id = int(notification_id)).update(is_read=True)
            return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)
        except Exception as e :
            return Response({"message":0,"error":f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

#10/01/2024
class TermsAndConditionView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        user_id = request.user.id      
        std_obj = Student.objects.get(user_id=user_id)
        message = 1 if std_obj.terms_condition else 0
        return Response({"message":message}, status=status.HTTP_200_OK)
    def post(self, request):
        user_id = request.user.id      
        std_obj = Student.objects.get(user_id=user_id)
        terms_conditions = request.data.get('terms_conditions', False)
        if not std_obj.terms_condition:
            std_obj.terms_condition = terms_conditions
            std_obj.save()
            return Response({"message":1}, status=status.HTTP_200_OK)
        else:
            return Response({"message":0}, status=status.HTTP_400_BAD_REQUEST)
