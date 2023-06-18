from channels.consumer import AsyncConsumer
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer, AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
import json

sockets = []

async def connectPlayer(self, data_player):
    global sockets
    for socket in sockets:

        if (self != socket['socket']):
            data = {
                "type": "websocket.send",
                "text": json.dumps
                ({
                    'status': 'connect',
                    'id': data_player['id']
                })
            }
            await socket['socket'].send(data)

async def movePlayer(self, data_player):
    global sockets
    for socket in sockets:

        if (self != socket['socket']):
            data = {
                "type": "websocket.send",
                "text": json.dumps
                ({
                    'status': 'move',
                    'id': data_player['id'],
                    'key': data_player['key']
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
                    'username': json.loads(event['text'])['username']
                }
                sockets.append(data)

                return
        except:
            pass

        data = json.loads(event['text'])

        if (data['status']):
            if (data['status'] == 'connect'):
                await connectPlayer(self, data)
                return
            
            if (data['status'] == 'move'):
                await movePlayer(self, data)
                return
            



        for socket in sockets:

            data = {
                "type": "websocket.send",
                "text": event['text']
            }
            await socket['socket'].send(data)

    async def websocket_disconnect(self, event):
        global sockets
        if (self in sockets):
            sockets.remove(self)

    


    
