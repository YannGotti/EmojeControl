from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
import json

sockets = []


async def updateData(self, data_user):
    global sockets
    for socket in sockets:
        if (socket['socket'] != self):
            data = {
                "type": "websocket.send",
                "text": json.dumps
                ({
                    'status': 'updateData',
                    'data': data_user
                })
            }
            await socket['socket'].send(data)

class Dispatcher(AsyncConsumer):

    async def websocket_connect(self, event):       
        await self.send({"type": "websocket.accept"})

    async def websocket_receive(self, event):
        global sockets
        
        try:
            if (json.loads(event['text'])['auth']):

                data = {
                    'socket' : self,
                    'username': json.loads(event['text'])['username'],
                    'id' : json.loads(event['text'])['id']
                }
                sockets.append(data)

                return
        except:
            pass

        data = json.loads(event['text'])

        await updateData(self, data)
        

    async def websocket_disconnect(self, event):
        global sockets
        

        if (self in sockets):
            sockets.remove(self)

    


    
