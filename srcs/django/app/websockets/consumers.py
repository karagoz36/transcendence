from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import json
import asyncio
from .pong import gameLoop, redisClient
from utils.friends import getFriends
from utils.users import onlineUsers, userIsLoggedIn
from database.models import getFriendship

class BaseConsumer(AsyncWebsocketConsumer):
    def __init__(self, consumerName: str):
        super().__init__()
        self.consumerName = consumerName

    async def connect(self):
        user: User = self.scope.get("user")
    
        if user is None or user.username == "":
            self.group_name = "unauthenticated"
            await self.close(code=4000)
            print(f"WebSocket: {self.group_name} closed", flush=True)
            return

        self.group_name = f"{user.id}_{self.consumerName}"

        await self.accept()
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        print(f"WebSocket: {self.group_name} connected", flush=True)

    async def disconnect(self, close_code):
        print(f"WebSocket: {self.group_name} disconnected", flush=True)

    async def receive(self, text_data: str):
        pass

    async def sendMessage(self, event):
        message: str = event["message"]
        await self.send(message)

    async def closeConnection(self, event):
        await self.close(code=4000)

class Notification(BaseConsumer):
    def __init__(self):
        super().__init__("notifications")

    async def connect(self):
        await super().connect()
        user: User = self.scope.get("user")
        if user is None:
            await self.close(code=4000)
            return
        if user.username == "":
            return
        onlineUsers[user.id] = True

        friends = await getFriends(user)
        for friend in friends:
            receiver: User = await User.objects.aget(id=friend["id"])
            message = json.dumps({
                "message": f"{user.username} logged in.",
                "link": "/friends/",
                "refresh": ["/friends/", "/pong/"]
                })
            await sendMessageWS(receiver, "notifications", message)

    async def disconnect(self, close_code):
        await super().disconnect(close_code)

        user: User = self.scope.get("user")
        if user is None:
            return
        if user.username == "":
            return
        if user.id in onlineUsers:
            del onlineUsers[user.id]

        friends = await getFriends(user)
        for friend in friends:
            receiver: User = await User.objects.aget(id=friend["id"])
            message = json.dumps({
                "message": f"{user.username} logged out.",
                "link": "/friends/",
                "refresh": ["/friends/", "/pong/"]
                })
            await sendMessageWS(receiver, "notifications", message)

class Messages(BaseConsumer):
    def __init__(self):
        super().__init__("messages")

class Pong(BaseConsumer):
    def __init__(self):
        super().__init__("pong")
        self.opponent: User|None = None
        self.user: User|None = None

    async def acceptInvite(self):
        try:
            opponent: User = await User.objects.aget(username=self.data.get("opponent"))
        except:
            return sendMessageWS(self.user, "pong", "failed to find opponent")

        if not userIsLoggedIn(opponent):
            return sendMessageWS(self.user, "pong", json.dumps({"type": "error", "error": "opponent not logged in"}))

        if await getFriendship(self.user, opponent) is None:
            return sendMessageWS(self.user, "pong", json.dumps({"type": "error", "error": "you are not friend with this user"}))

        self.opponent = opponent
        await sendMessageWS(opponent, "pong", json.dumps({"type": "invite_accepted", "friend": self.user.username}))

    async def receive(self, text_data: str):
        await super().receive(text_data)
        self.user: User = self.scope["user"]

        if self.user.is_anonymous:
            return sendMessageWS(self.user, "pong", json.dumps({"type": "error", "error": "not logged in"}))

        try:
            self.data = json.loads(text_data)
        except:
            return sendMessageWS(self.user, "pong", json.dumps({"type": "error", "error": "invalid message"}))

        if type(self.data) is not dict:
            return sendMessageWS(self.user, "pong", json.dumps({"type": "error", "error": "invalid message"}))

        match self.data.get("type"):
            case "accept_invite":
                await self.acceptInvite()

            case "launch_game":
                if self.opponent is None:
                    err = {"type": "error", "error": "trying to launch a game without an opponent"}
                    return sendMessageWS(self.user, "pong", json.dumps(err))
                htmlSTR = render_to_string("pong/play.html")
                await sendMessageWS(self.opponent, "pong", json.dumps({"type": "launch_game", "html": htmlSTR}))
                await sendMessageWS(self.user, "pong", json.dumps({"type": "launch_game", "html": htmlSTR}))
                asyncio.create_task(gameLoop(self.user, self.opponent))

            case "join_game":
                htmlSTR = render_to_string("pong/play.html")
                await sendMessageWS(self.opponent, "pong", json.dumps({"type": "launch_game", "html": htmlSTR}))

            case "move":
                key = f"pong_direction:{self.user.id}"

                match self.data.get("direction"):
                    case "up":
                        redisClient.hmset(key, {"direction": "up"})
                    case "down":
                        redisClient.hmset(key, {"direction": "down"})
                    case _:
                        redisClient.delete(key)
