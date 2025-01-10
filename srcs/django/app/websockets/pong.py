import json
import asyncio
import math
import redis
from django.contrib.auth.models import User
from utils.websocket import sendMessageWS

redisClient = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

class Vector2:
    x: float
    y: float

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = x
        self.y = y
    
    def abs(self) -> "Vector2":
        return Vector2(abs(self.x), abs(self.y))


e_direction = {
    "NONE": 0,
    "TOP": 1,
    "BOTTOM": 2,
}

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
    
    def collidedTop(self, pos: Vector2) -> bool:
        playerPos = self.pos.abs()
        ballPos = pos.abs()
        return ballPos.y >= playerPos.y - self.width / 2 and ballPos.y <= playerPos.y
    
    def collidedBottom(self, pos: Vector2) -> bool:
        playerPos = self.pos.abs()
        ballPos = pos.abs()
        return ballPos.y <= playerPos.y + self.width / 2 and ballPos.y >= playerPos.y

    def collided(self, pos: Vector2) -> int:
        playerPos = self.pos.abs()
        ballPos = pos.abs()

        if playerPos.x >= ballPos.x:
            return False

        if self.collidedBottom(pos):
            return e_direction["BOTTOM"]
        if self.collidedTop(pos):
            return e_direction["TOP"]
        return e_direction["NONE"]

    def get_relative_impact(self, ball_y: float) -> float:
        #normalise la taille du pad et trouver la valeur pour le calcul de l'angle
        relative_impact = (ball_y - self.pos.y) / (self.width / 2)
        return max(-1.0, min(1.0, relative_impact))

class Ball:
    velocity = Vector2(0.2, 0)
    pos: Vector2 = Vector2()
    p1: PongPlayer
    p2: PongPlayer
    field_height: float = 15.0

    def __init__(self, p1: PongPlayer, p2: PongPlayer):
        self.p1 = p1
        self.p2 = p2

    def scored(self) -> bool:
        if self.pos.x >= self.p1.pos.x + 1:
            return True
        if self.pos.x <= self.p2.pos.x - 1:
            return True
        return False

    def check_walls(self):
        if self.pos.y >= self.field_height / 2:  # Mur du haut
            self.velocity.y *= -1
            self.pos.y = self.field_height / 2
        elif self.pos.y <= -self.field_height / 2:  # Mur du bas
            self.velocity.y *= -1
            self.pos.y = -self.field_height / 2

    def reset_ball(self):
        self.pos = Vector2(0, 0)
        self.velocity = Vector2(0.2, 0)

    def move(self):
        if self.scored():
            self.reset_ball()
            return

        self.check_walls()

        if self.pos.x > 0 and self.p1.collided(self.pos) != 0:
            relative_impact = self.p1.get_relative_impact(self.pos.y)
            angle = relative_impact * (math.pi / 3)
            speed = math.sqrt(self.velocity.x**2 + self.velocity.y**2)
            self.velocity.x = -speed * math.cos(angle)
            self.velocity.y = speed * math.sin(angle)

        elif self.pos.x < 0 and self.p2.collided(self.pos) != 0:
            relative_impact = self.p2.get_relative_impact(self.pos.y)
            angle = relative_impact * (math.pi / 3)
            speed = math.sqrt(self.velocity.x**2 + self.velocity.y**2)
            self.velocity.x = speed * math.cos(angle)
            self.velocity.y = speed * math.sin(angle)

        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y

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
