from django.shortcuts import render

## add chat
def index(request):
    data = [
        {
            "username":"Admin",
            "id": 200,
            "room_id": 1
        },
        {
            "username":"Admin",
            "id": 200,
            "room_id": 1
        },
        {
            "username":"Admin",
            "id": 200,
            "room_id": 1
        }
    ]
    return render(request, "chat/index.html", {"data":data})



def room(request, room_id):
    return render(request, "chat/chat.html", {"room_id": room_id})


# class InstructorSubmissionPointAllViewList(ListAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)

#     def get(self, request):
#         try:
#             batch_id = request.GET.get('batch_id')            
#             week_id = request.GET.get('week_id') 
#             ongoing_data = TaskSubmission.objects.filter(batch_id=batch_id, week=week_id, batch__completed=False).values(
#                 "id", "batch_id", "student_userfirst_name", "studentuser_last_name", "week",
#                 "course_submission__submission_topic","file","status", "created_at"
#             ).order_by("-id")
#             assigned_projects = BatchJoined.objects.filter(batch_id=batch_id).values(
#                 'student_userfirst_name', 'studentuser_last_name',
#                 'assign_topic_project_topic', 'assign_project_project_name'
#             )
#             topic_by_student = {f"{project['student_userfirst_name']} {project['studentuser_last_name']}": {
#                 'assigned_project': project.get('assign_project__project_name', None),
#                 'assigned_topic': project.get('assign_topic__project_topic', None),
#             } for project in assigned_projects}
            
#             ongoing_grouped_data = []
#             previous_grouped_data = []

#             for entry in ongoing_data:
#                 student_name = f"{entry['student_userfirst_name']} {entry['studentuser_last_name']}"
#                 assigned_info = topic_by_student.get(student_name, {'assigned_project': None, 'assigned_topic': None})
                
#                 entry_info = {
#                     "id": entry["id"],
#                     "batch_id": entry["batch_id"],
#                     "course_submission_submission_topic": entry["course_submission_submission_topic"],
#                     "student_userfirst_name": entry["studentuser_first_name"],
#                     "student_userlast_name": entry["studentuser_last_name"],
#                     "week": entry["week"],
#                     "assigned_project": assigned_info['assigned_project'],
#                     "assigned_topic": assigned_info['assigned_topic'],
#                     # "file":  file_url,
#                     "file": TaskSubmission.objects.filter(batch_id=batch_id, week=week_id, batch__completed=False).first().file.url,
#                     "status": entry['status'],
#                     "created_at": entry["created_at"],
#                 }

#                 ongoing_grouped_data.append(entry_info)

#             previous_data = TaskSubmission.objects.filter(batch_id=batch_id, week=week_id, batch__completed=True).values(
#                 "id", "batch_id", "student_userfirst_name", "studentuser_last_name", "week",
#                 "course_submission__submission_topic","file","status", "created_at"
#             ).order_by("id")

#             for entry in previous_data:
#                 student_name = f"{entry['student_userfirst_name']} {entry['studentuser_last_name']}"
#                 assigned_info = topic_by_student.get(student_name, {'assigned_project': None, 'assigned_topic': None})
#                 entry_info = {
#                     "id": entry["id"],
#                     "batch_id": entry["batch_id"],
#                     "course_submission_submission_topic": entry["course_submission_submission_topic"],
#                     "student_userfirst_name": entry["studentuser_first_name"],
#                     "student_userlast_name": entry["studentuser_last_name"],
#                     "week": entry["week"],
#                     "assigned_project": assigned_info['assigned_project'],
#                     "assigned_topic": assigned_info['assigned_topic'],
#                     # "file": file_url,
#                     "file":  TaskSubmission.objects.filter(batch_id=batch_id, week=week_id, batch__completed=True).first().file.url,
#                     "status": entry['status'],
#                     "created_at": entry["created_at"],
#                 }

#                 previous_grouped_data.append(entry_info)
    
#             return Response({"message":1,"ongoing_data": ongoing_grouped_data, "previous_data": previous_grouped_data}, status=status.HTTP_200_OK)  
#         except Exception as e:
#             return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)


