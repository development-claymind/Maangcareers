from django.urls import path
from .views import *


urlpatterns = [ 
    path('chat/', index, name='chat'),
    path("chat/<int:room_id>/", room, name="room"),
]