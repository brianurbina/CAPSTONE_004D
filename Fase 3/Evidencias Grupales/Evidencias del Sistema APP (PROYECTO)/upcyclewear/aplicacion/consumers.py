import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversacion_id = self.scope['url_route']['kwargs']['conversacion_id']
        self.room_group_name = f'chat_{self.conversacion_id}'

        # Unirse a la sala de chat
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Salir de la sala de chat
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        mensaje = text_data_json['mensaje']
        emisor = text_data_json['emisor']  # Agrega el emisor al mensaje
        foto = text_data_json['foto']  # Agrega la foto al mensaje
        hora = text_data_json['hora']  # Agrega la hora al mensaje

        # Enviar mensaje a la sala de chat
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'mensaje': mensaje,
                'emisor': emisor,
                'foto': foto,
                'hora': hora,
            }
        )

    async def chat_message(self, event):
        mensaje = event['mensaje']
        emisor = event['emisor']
        foto = event['foto']  # Recibe la foto
        hora = event['hora']  # Recibe la hora

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'mensaje': mensaje,
            'emisor': emisor,
            'foto': foto,  # Enviar la foto
            'hora': hora,  # Enviar la hora
        }))
