from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.template.loader import render_to_string
import json
import asyncio
from .pong import gameLoop, redisClient, PongPlayer, Ball
from utils.friends import getFriends
from utils.users import onlineUsers, userIsLoggedIn
from database.models import getFriendship
from utils.websocket import sendMessageWS

class BaseConsumer(AsyncWebsocketConsumer):
    def __init__(self, consumerName: str):
        super().__init__()
        self.consumerName = consumerName

    async def connect(self):
        user: User = self.scope.get("user")
    
        await self.accept()
        if user is None or user.username == "":
            self.group_name = "unauthenticated"
            await self.close(code=4000)
            print(f"WebSocket: {self.group_name} closed", flush=True)
            return

        self.group_name = f"{user.id}_{self.consumerName}"

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
        onlineUsers[user.id] = user

        friends = await getFriends(user)
        for friend in friends:
            receiver: User = await User.objects.aget(id=friend.id)
            message = json.dumps({
                "message": f"{user.username} logged in.",
                "refresh": ["/friends/", "/pong/", "/tournament/create/"]
                })
            await sendMessageWS(receiver, "notifications", message)

    async def disconnect(self, close_code):
        await super().disconnect(close_code)

        user: User = self.scope.get("user")
        if user is None:
            return
        if user.username == "":
            return
        if userIsLoggedIn(user):
            del onlineUsers[user.id]

        friends = await getFriends(user)
        for friend in friends:
            receiver: User = await User.objects.aget(id=friend.id)
            message = json.dumps({
                "message": f"{user.username} logged out.",
                "refresh": ["/friends/", "/pong/", "/tournament/create/"]
                })
            await sendMessageWS(receiver, "notifications", message)

class Messages(BaseConsumer):
    def __init__(self):
        super().__init__("messages")

class LocalGamer:
    def __init__(self, username='LocalGamer'):
        self.username = username
        self.is_local = True
        self.id = 99999
        self.score: int = 0

    def __eq__(self, other):
        return isinstance(other, LocalGamer)
    
    def __hash__(self):
        return hash('LocalGamer')

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
            await sendMessageWS(self.user, "pong", json.dumps({"type": "error", "error": "not logged in"}))
            return

        try:
            self.data = json.loads(text_data)
        except:
            await sendMessageWS(self.user, "pong", json.dumps({"type": "error", "error": "invalid message"}))
            return

        if type(self.data) is not dict:
            await sendMessageWS(self.user, "pong", json.dumps({"type": "error", "error": "invalid message"}))
            return

        match self.data.get("type"):
            case "accept_invite":
                await self.acceptInvite()

            case "launch_game":
                if self.opponent is None:
                    err = {"type": "error", "error": "trying to launch a game without an opponent"}
                    await sendMessageWS(self.user, "pong", json.dumps(err))
                    return
                htmlSTR = render_to_string("pong/play.html")
                launch_data = {
                    "type": "launch_game",
                    "html": htmlSTR,
                    "player": self.user.username,
                    "opponent": self.opponent.username,
                    "initiator": self.user.username,
				}
                launch_data_opponent = {
                    "type": "launch_game",
                    "html": htmlSTR,
                    "player": self.opponent.username,
                    "opponent": self.user.username,
                    "initiator": self.user.username,
				}
                await sendMessageWS(self.opponent, "pong", json.dumps(launch_data))
                await sendMessageWS(self.user, "pong", json.dumps(launch_data_opponent))
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

class PongSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.p1 = PongPlayer(LocalGamer("p1"), 10)
        self.p2 = PongPlayer(LocalGamer("p2"), -10)
        self.ball = Ball(self.p1, self.p2, False)
        self.p1.score = 0
        self.p2.score = 0
        self.ball.ball_start()
        htmlSTR = render_to_string("pong/localplay.html")
        await self.send(json.dumps({"type": "launch_game", "html": htmlSTR}))
        self.game_running = True
        asyncio.create_task(self.start_game_loop())

    async def disconnect(self, close_code):
        self.game_running = False

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(json.dumps({"error": "Invalid JSON format"}))
            return

        match data.get("type"):
            case "move":
                await self.handle_move(data)
            case "player_exit":
                self.game_running = False
            case _:
                await self.send(json.dumps({"error": "Unknown message type"}))

    async def handle_move(self, data):
        direction = data.get("direction", "none")
        player = data.get("player", "none")
        
        if isinstance(self.p1.user, LocalGamer) or isinstance(self.p2.user, LocalGamer):
            key = f"pong_direction:{player}"
        else:
            key = f"pong_direction:{self.p1.user.id if player == 'p1' else self.p2.user.id}"

        if direction in ["up", "down"]:
            redisClient.hmset(key, {"direction": direction})
        else:
            redisClient.delete(key)

    async def start_game_loop(self):
        while self.game_running:
            self.p1.move_key()
            self.p2.move_key()
            self.ball.move()
            hit_detected = False
            if self.p1.score == 3 or self.p2.score == 3:
                data = {"type": "game_over"}
                await self.send(json.dumps(data))
                self.p1.score = 0
                self.p2.score = 0
                self.game_running = False
                break
            if self.ball.pos.x > 0 and self.p1.collided(self.ball.pos) != 0:
                hit_detected = True
            elif self.ball.pos.x < 0 and self.p2.collided(self.ball.pos) != 0:
                hit_detected = True
            data = {
                "type": "update_pong",
                "p1": {"x": self.p1.pos.x, "y": self.p1.pos.y},
                "p2": {"x": self.p2.pos.x, "y": self.p2.pos.y},
                "ball": {"x": self.ball.pos.x, "y": self.ball.pos.y},
                "score": {"p1": self.p1.score, "p2": self.p2.score}
            }
            if hit_detected:
                data["type"] = "hitBall"
            if self.game_running == False:
                break

            await self.send(json.dumps(data))
            await asyncio.sleep(1 / 60)