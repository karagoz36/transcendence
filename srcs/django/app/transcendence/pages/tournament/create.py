from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.friends import getFriends
from utils.websocket import sendMessageWS
from typing import Tuple
import math
import json

class Tournament:
    organizer: User
    public: bool = False
    players: dict[int, User] = {}
    invited: dict[int, User] = {}
    games: list[Tuple[User, User]] = []
    started: bool = False

    def __init__(self, organizer: User):
        self.organizer = organizer
        self.players[organizer.id] = organizer
    
    async def inviteUser(self, invited: User):
        self.invited[invited.id] = invited
        msg = {
            "message": f"<a href='/tournament/lobby/?id={self.organizer.id}'>{self.organizer.username} invited you to its tournament</a>",
            "refresh": ["/"]
            }
        await sendMessageWS(invited, "notifications", json.dumps(msg))

    async def removePlayer(self, player: User):
        if player.id == self.organizer.id:
            return await self.deleteTournament()

        try: self.invited.pop(player.id)
        except: pass

        try: self.players.pop(player.id)
        except: pass
    
    async def addPlayer(self, player: User):
        del self.invited[player.id]
        self.players[player.id] = player
        msg = {"message": f"{player.username} accepted your invitation to your tournament", "refresh": ["/tournament/create/"]}
        await sendMessageWS(self.organizer, "notifications", json.dumps(msg))
    
    async def deleteTournament(self):
        tournaments.pop(self.organizer.id)
        msg = {"message": f"{self.organizer.username} deleted its tournament", "refresh": ["/tournament/create/", "/tournament/lobby/", "/"]}
        msg = json.dumps(msg)
    
        for player in self.players.values():
            await sendMessageWS(player, "notifications", msg)
    
        for player in self.invited.values():
            await sendMessageWS(player, "notifications", msg)

    def userInvited(self, user: User) -> bool:
        return self.invited.get(user.id) != None
    
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

        while i < len(self.players):
            if i + 1 == len(self.players):
                break
            self.games.append((self.players[i], self.players[i + 1]))
            i += 2
    
    def launchGame(self):
        self.started = True
        self.createGames()

tournaments: dict[int, Tournament] = {}

@login_required(login_url="/api/logout")
async def response(request: Request) -> Response:
    user: User = request.user
    friends = await getFriends(user)

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

    for friend in friends:
        if tournament.userInvited(friend) or tournament.userJoined(friend):
            friends.remove(friend)
    return render(request, "tournament/create.html", {
        "friends": friends, "ERROR": error, "SUCCESS": success,
        "players": tournament.players.values(), "organizer": tournament.organizer
        })