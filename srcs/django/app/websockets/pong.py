import asyncio
import redis
from django.contrib.auth.models import User
import json
from utils.websocket import sendMessageWS

redisClient = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

class PongPlayer:
    user: User
    position: float = 0.0

    def __init__(self, user: User):
        self.user = user
        
    def move(self):
        key = f"pong_direction:{self.user.id}"
        direction = redisClient.hgetall(key)
        direction = direction.get("direction")
        if direction is None:
            print('no direction', flush=True)
            return
        redisClient.delete(key)

async def gameLoop(user1: User, user2: User):
    p1 = PongPlayer(user1)
    p2 = PongPlayer(user2)

    while True:
        p1.move()
        p2.move()
        await asyncio.sleep(1 / 30)