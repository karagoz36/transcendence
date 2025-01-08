import json
import asyncio
import redis
from django.contrib.auth.models import User
from utils.websocket import sendMessageWS

redisClient = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

class PongPlayer:
    user: User
    x: float
    y: float = 0.0

    def __init__(self, user: User, x: float):
        self.user = user
        self.x = x
        
    def move(self):
        key = f"pong_direction:{self.user.id}"
        direction = redisClient.hgetall(key)
        direction: str|None = direction.get("direction")
        match direction:
            case "up":
                self.y += 0.5
            case "down":
                self.y -= 0.5
            case None:
                return        
        redisClient.delete(key)

async def gameLoop(user1: User, user2: User):
    p1 = PongPlayer(user1, 10)
    p2 = PongPlayer(user2, -10)

    while True:
        p1.move()
        p2.move()
        data = {
            "type": "update_pong",
            "p1": {"x": p1.x, "y": p1.y},
            "p2": {"x": p2.x, "y": p2.y},
            "ball": {"x": 0, "y": 0}
        }
        await sendMessageWS(p1.user, "pong", json.dumps(data))
        await sendMessageWS(p2.user, "pong", json.dumps(data))
        await asyncio.sleep(1 / 30)