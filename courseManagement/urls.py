# from .views import CourseViewSet, TimeTableViewSet, UserBatchViewSet, PaymentViewSet, NoteViewSet, CertificateViewSet,StudentClassTimeTableViewSet
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register('list-courses', CourseViewSet, basename='list-courses')
# router.register('list-notes', NoteViewSet, basename='list-notes')
# router.register('list-certificates', CertificateViewSet, basename='list-certificate')
urlpatterns = [
    # path('list-courses/', CourseViewSet.as_view(), name='list-courses'),
    path('timetable/', TimeTableViewSet.as_view(), name='timetable'),
    path('list-notes/', NoteViewSet.as_view(), name='list-notes'),
    path('list-certificates/', CertificateViewSet.as_view(), name='list-certificates'),
    path('user-batch/', UserBatchViewSet.as_view(), name='user-batch'),
    path('payment-status/', PaymentViewSet.as_view({'post':'create'}), name='payment-status'),
    path('stud-timetable-list/', StudentClassTimeTableViewSet.as_view(), name='stud-timetable-list'),
    path('stud-routine-list/', StudentClassesRoutineViewSet.as_view(), name='stud-routine-list'),
    path('stud-project-assign/<int:b_id>', StudentProjectAssign.as_view(), name='stud-project-assign'),
] + router.urls
