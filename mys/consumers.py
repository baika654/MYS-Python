# chat/consumers.py

import json
from channels.generic.websocket import WebsocketConsumer
class ChatConsumer(WebsocketConsumer):
    
    connections = []

    def connect(self):
        print("JS routine has connected to channel")
        self.accept()
        self.send(text_data = json.dumps({"type": "chat.message","message": "Starting WebSocket"}))
        ChatConsumer.connections.append(self)
    def disconnect(self, close_code):
        pass
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        self.send(text_data=json.dumps({
            'message': message
        }))
    def sendMessage(self, text_data):
        self.send(text_data = json.dumps({"type": "chat.message","message": text_data}))
    @staticmethod
    def getChannelToBrowser():
        if (len(ChatConsumer.connections)!=0):
            return ChatConsumer.connections[0]
        else:
            return None    
    