import json
from . import views
from channels.generic.websocket import AsyncWebsocketConsumer

#used to store group names
groups=""

#used to store group messages
group_messages={}

class ChatConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user=views.UserID
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        global groups
        if self.room_name!="lobby" and self.room_name not in groups:
            groups+='<a href="/chat/'+self.room_name+'/?name='+self.room_name+'&user={user}"><div class="chat_list active_chat"><div class="chat_people"><div class="chat_img"> <img src="https://iconape.com/wp-content/png_logo_vector/android-messages.png" alt="sunil"> </div><div class="chat_ib"><h5>'+self.room_name+'</h5></div></div></div></a>'
        await self.send(text_data=json.dumps(
        {
            'message': groups
        }))
        try:
            await self.send(text_data=json.dumps(
            {
                'message': group_messages[self.room_name]
            }))
        except:
            pass

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if "chat_list" not in message:
            try:
                group_messages[self.room_name]+=message
            except:
                group_messages[self.room_name]=message
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps(
        {
            'message': message
        }))