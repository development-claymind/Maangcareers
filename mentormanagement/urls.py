from django.urls import path
from .views import *


urlpatterns = [ 
    path('terms-condition/', InstructorTermsAndConditionView.as_view(), name='terms-condition'),
    path('rules-regulation/', InstructorRulesAndRegulationView.as_view(), name='rules-regulation'),

    # mentor profile
    path('inst-profile/<pk>', InstructorProfileViewSet.as_view(), name='inst-profile'), ####
    path('inst-profilepasswordupdate/', InstructorProfilePasswordUpdate.as_view(), name='inst-profilepasswordupdate'),
    path('inst-profileinfo/', InstructorProfileInfo.as_view(), name='inst-profileinfo'),
    path('inst-profiledetailsupdate/', InstructorProfileDetailsUpdate.as_view(), name='inst-profiledetailsupdate'),

    #dashboard
    path('inst-calender-view/', InstructorDashboardCalenderViewList.as_view(), name='inst-calender-view'), #19/01/2024
    path('inst-cls-complete/', InstructorClassCompleteProgressBar.as_view(), name='inst-cls-complete'),  #19/01/2024
    path('inst-ongoing-upcomig/', InstructorDashboardOngoingUpcomingUpdates.as_view(), name='inst-ongoing-upcomig'),
    path('inst-timetable/', InstructorTimetableViewList.as_view(), name='inst-timetable'), 

    #24/01/2024
    path('inst-course/', InstructorCourseSelection.as_view(), name='inst-course'),
    path('inst-get-batch/', InstructorOngoingPreviousBatchSelection.as_view(), name='inst-get-batch'),

    # Teaching section 
    path('inst-week-notes/', InstructorAllNotesWeekLock.as_view(), name='inst-week-notes'),
    path('inst-practice-week-lock/', InstructorTeachingPracticeWeekLock.as_view(), name='inst-practice-week-lock'),
    
    
    # path('requ/', batch_complete_request_list, name='batch_complete_request_list'),
    # path('requ2/', create_batch_complete_request, name='create_batch_complete_request'),
    

]