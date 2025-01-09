import json
import asyncio
import redis
from django.contrib.auth.models import User
from utils.websocket import sendMessageWS

redisClient = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

class Vector2:
    pass

class Vector2:
    x: float
    y: float

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y
    
    def abs(self) -> Vector2:
        return Vector2(abs(self.x), abs(self.y))

class PongPlayer:
    user: User
    width: float = 3
    pos: Vector2

    def __init__(self, user: User, x: float):
        self.user = user
        self.pos = Vector2(x)
        
    def move(self):
        key = f"pong_direction:{self.user.id}"
        direction = redisClient.hgetall(key)
        direction: str | None = direction.get("direction")
        match direction:
            case "up":
                self.pos.y += 0.25
            case "down":
                self.pos.y -= 0.25
            case None:
                return        
        redisClient.delete(key)

    def collided(self, pos: Vector2) -> bool:
        playerPos = self.pos.abs()
        ballPos = pos.abs()
        if playerPos.x >= ballPos.x:
            return False
        return ballPos.y >= playerPos.y - self.width / 2 and ballPos.y <= playerPos.y + self.width / 2

class Ball:
    velocity = Vector2(0.2)
    pos: Vector2 = Vector2()
    p1: PongPlayer
    p2: PongPlayer

    def __init__(self, p1: PongPlayer, p2: PongPlayer):
        self.p1 = p1
        self.p2 = p2

    def scored(self) -> bool:
        if self.pos.x >= self.p1.pos.x + 1:
            return True
        if self.pos.x <= self.p2.pos.x - 1:
            return True
        return False

    def move(self):
        if self.scored():
            self.pos.x = 0
            self.pos.y = 0

        if self.pos.x > 0 and self.p1.collided(self.pos):
            self.velocity.x *= -1
            self.velocity.y *= -1
        elif self.pos.x < 0 and self.p2.collided(self.pos):
            self.velocity.x *= -1
            self.velocity.y *= -1

        self.pos.y += self.velocity.y
        self.pos.x += self.velocity.x


async def gameLoop(user1: User, user2: User):
    p1 = PongPlayer(user1, 10)
    p2 = PongPlayer(user2, -10)
    ball = Ball(p1, p2)

    while True:
        p1.move()
        p2.move()
        ball.move()

        data = {
            "type": "update_pong",
            "p1": {"x": p1.pos.x, "y": p1.pos.y},
            "p2": {"x": p2.pos.x, "y": p2.pos.y},
            "ball": {"x": ball.pos.x, "y": ball.pos.y}
        }
        await sendMessageWS(p1.user, "pong", json.dumps(data))
        await sendMessageWS(p2.user, "pong", json.dumps(data))
        await asyncio.sleep(1 / 60)