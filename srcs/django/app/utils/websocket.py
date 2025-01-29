from channels.layers import get_channel_layer, BaseChannelLayer
from django.contrib.auth.models import User

async def sendMessageWS(receiver: User, groupName: str, message: str) -> None:
    layer: BaseChannelLayer = get_channel_layer()
    await layer.group_send(f"{receiver.id}_{groupName}", {
        "type": "sendMessage",
        "message": message
        })