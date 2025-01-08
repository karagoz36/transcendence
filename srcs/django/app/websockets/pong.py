import asyncio
import redis
from django.contrib.auth.models import User

redisClient = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

class PongPlayer:
    user: User
    position: float = 0.0

    def __init__(self, user: User):
        self.user = user
        
    def move(self):
        key = f"pong_direction:{self.user.id}"
        direction = redisClient.hgetall(key)
        direction: str|None = direction.get("direction")
        match direction:
            case "up":
                self.position += 1
            case "down":
                self.position -= 1
            case None:
                return        
        redisClient.delete(key)
        print(self.position, flush=True)

async def gameLoop(user1: User, user2: User):
    p1 = PongPlayer(user1)
    p2 = PongPlayer(user2)

    while True:
        p1.move()
        p2.move()
        await asyncio.sleep(1 / 30)