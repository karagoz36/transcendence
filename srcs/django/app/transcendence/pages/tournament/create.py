from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.friends import getFriends
from utils.websocket import sendMessageWS
import math
import json
import asyncio
from websockets.pong import gameLoop
from asyncio import Task
from utils.users import notifEveryone

class GameData:
    p1: User
    p2: User
    started: bool

class Tournament:
    organizer: User
    public: bool = False
    players: dict[int, User]
    games: list[GameData]
    started: bool
    waitTime = 10

    def __init__(self, organizer: User):
        self.organizer = organizer
        self.players = {organizer.id: organizer}
        self.games = []
        self.started = False

    async def removePlayer(self, player: User):
        if player.id == self.organizer.id:
            return await self.deleteTournament()

        msg = {
            "message": f"{player.username} left {self.organizer.username}'s tournament",
            "refresh": ["/", "/tournament/create/", f"/tournament/lobby/?id={self.organizer.id}"]
        }
        self.players.pop(player.id)
        await self.sendNotifToPlayers(msg)
        await sendMessageWS(player, "notifications", json.dumps({ "redirect": "/" }))
    
    async def addPlayer(self, player: User):
        if self.userJoined(player):
            return
        self.players[player.id] = player
        await self.sendNotifToPlayers({
            "message": f"{player.username} joined {self.organizer.username}'s tournament",
            "refresh": ["/tournament/create/", f"/tournament/lobby/?id={self.organizer.id}"]
        })

    async def deleteTournament(self):
        tournaments.pop(self.organizer.id)
        await self.sendNotifToPlayers({
            "message": f"{self.organizer.username}'s tournament deleted",
            "redirect": "/"
        }, [self.organizer])
        await notifEveryone({"refresh": "/"}, [self.organizer])

    def userJoined(self, user: User) -> bool:
        return self.players.get(user.id) != None

    # In a single-elimination tournament where the number of players is not even,
    # some players will receive a bye in the first round.
    # A bye allows a player to advance to the next round without competing in that round.
    def getNumberOfByes(self) -> int:
        nextPowerOf2 = 2 ** math.ceil(math.log2(len(self.players)))
        byes = nextPowerOf2 - len(self.players)
        return byes

    def createGames(self):
        i = self.getNumberOfByes()
        players = list(self.players.values())

        while i < len(players):
            if i + 1 == len(players):
                break
            data = GameData()
            data.p1 = players[i]
            data.p2 = players[i + 1]
            data.started = False
            self.games.append(data)
            i += 2
    
    async def startGames(self):
        htmlSTR = render_to_string("pong/play.html")

        def onGameover(winner: User, game: GameData):
            self.games.pop(self.games.index(game))
            loser: User = game.p1 if game.p2 == winner else game.p2
            self.players.pop(loser.id)
            if len(self.players) == 1:
                tournaments.pop(self.organizer.id)
                print("TOURNAMENT OVER")
                return
            if len(self.games) == 0:
                self.launch()
                return

        for game in self.games:
            msg = json.dumps({"type": "launch_game", "html": htmlSTR})
            await sendMessageWS(game.p1, "pong", msg)
            await sendMessageWS(game.p2, "pong", msg)

            if game.started:
                return ""
            game.started = True
            task = asyncio.create_task(gameLoop(game.p1, game.p2))

            def callback(task: Task[User]):
                onGameover(task.result(), game)

            task.add_done_callback(callback)
    
    async def announceGames(self):
        format = f"You will play against $OPPONENT in {self.organizer.username}'s tournament in {self.waitTime} seconds."
        dict = {"message": format, "redirect": f"/tournament/lobby/?id={self.organizer.id}"}

        for game in self.games:
            notif = format.replace("$OPPONENT", game.p1.username)
            dict["message"] = notif
            message = json.dumps(dict)
            await sendMessageWS(game.p2, "notifications", message)

            notif = format.replace("$OPPONENT", game.p2.username)
            dict["message"] = notif
            message = json.dumps(dict)
            await sendMessageWS(game.p1, "notifications", message)

    async def launch(self):
        self.started = True
        self.createGames()
        await self.announceGames()
        await asyncio.sleep(self.waitTime)
        await self.startGames()

    async def sendNotifToPlayers(self, msg: dict, blacklist: list[User] = []):
        msg: str = json.dumps(msg)
        for player in self.players.values():
            if player not in blacklist:
                await sendMessageWS(player, "notifications", msg)
    
    def userHasGameRunning(self, user: User) -> bool:
        for game in self.games:
            if (game.p1 == user or game.p2 == user) and game.started:
                return True
        return False

tournaments: dict[int, Tournament] = {}

@login_required(login_url="/api/logout")
async def response(request: Request) -> Response:
    user: User = request.user

    error = request.query_params.get("error")
    if error is None:
        error = ""

    success = request.query_params.get("success")
    if success is None:
        success = ""

    tournament = tournaments.get(user.id)
    if tournament == None:
        tournament = Tournament(user)
        tournaments[user.id] = tournament
        await notifEveryone({"refresh": "/"}, [user])
    if tournament.started:
        return redirect("/tournament/lobby/")
    return render(request, "tournament/create.html", {
        "players": tournament.players.values(),
        "organizer": tournament.organizer,
        "ERROR": error,
    })
