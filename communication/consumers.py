import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User
from .models import Room, MessageBox

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope["url_route"]["kwargs"]["room_name"])
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        sender_user_id = text_data_json["sender_user_id"]
        reciver_user_id = text_data_json["reciver_user_id"]  # Optional field
        message = text_data_json["message"]
        # Get the sender user
        sender_user = User.objects.get(id=sender_user_id)
        reciver_user = User.objects.get(id=reciver_user_id)
        # Get the room associated with this consumer
        # print("check_room",self.room_name)
        room = Room.objects.get(id=int(self.room_name))

        # Save message to MessageBox
        message_box = MessageBox.objects.create(
            room=room,
            sender_user=sender_user,
            reciver_user=reciver_user,
            is_read=False,
            text_message=message,
            send_file=None,  # Update this based on your logic
            send_image=None,  # Update this based on your logic
        )

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
