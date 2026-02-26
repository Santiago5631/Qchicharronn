# menu/consumers.py  — ARCHIVO NUEVO
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import VistaConfig


class VistaCocinaConsumer(AsyncWebsocketConsumer):
    """
    Consumer WebSocket para las vistas de Parrilla y Cocina.
    URL: /ws/vista/<area>/   (area = 'parrilla' o 'cocina')
    """

    async def connect(self):
        self.area = self.scope['url_route']['kwargs']['area']

        if self.area not in ('parrilla', 'cocina'):
            await self.close()
            return

        self.group_name = f'vista_{self.area}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Al conectar, envía la config actual de categorías
        config = await self.get_config()
        await self.send(text_data=json.dumps({
            'type': 'config_inicial',
            'categorias_activas': config,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """Recibe mensajes del frontend (ej: cambio de categorías activas)"""
        data = json.loads(text_data)

        if data.get('action') == 'actualizar_categorias':
            # Guarda las nuevas categorías seleccionadas
            nuevas_ids = data.get('categoria_ids', [])
            await self.guardar_categorias(nuevas_ids)

            # Confirmar al cliente
            await self.send(text_data=json.dumps({
                'type': 'categorias_actualizadas',
                'categoria_ids': nuevas_ids,
            }))

    async def pedido_update(self, event):
        """Recibe pedidos nuevos/actualizados desde las signals y los reenvía al frontend"""
        await self.send(text_data=json.dumps({
            'type': 'pedido_update',
            'accion': event['accion'],
            'pedido': event['pedido'],
        }))

    @database_sync_to_async
    def get_config(self):
        """Retorna las categorías activas guardadas para esta vista"""
        config, _ = VistaConfig.objects.get_or_create(area=self.area)
        return list(
            config.categorias_activas.values('id', 'nombre')
        )

    @database_sync_to_async
    def guardar_categorias(self, categoria_ids):
        """Guarda las categorías seleccionadas en la base de datos"""
        from categoria.models import Categoria
        config, _ = VistaConfig.objects.get_or_create(area=self.area)
        config.categorias_activas.set(
            Categoria.objects.filter(id__in=categoria_ids)
        )