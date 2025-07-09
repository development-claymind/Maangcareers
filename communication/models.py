from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)
    user_one = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_one")
    user_two = models.ForeignKey(User, on_delete=models.CASCADE,related_name="user_two")

class MessageBox(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="room")
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender_user")
    reciver_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="reciver_user")
    is_read = models.BooleanField(default=False)
    text_message = models.TextField()
    send_file = models.FileField(upload_to="chat_file/")
    send_image = models.FileField(upload_to="chat_image/")
