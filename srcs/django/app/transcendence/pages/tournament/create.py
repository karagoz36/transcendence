from rest_framework.request import Request
from rest_framework.response import Response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from utils.friends import getFriends
from utils.websocket import sendMessageWS
import json

class Tournament:
    organizer: User
    public: bool = False
    players: dict[int, User] = {}
    invited: dict[int, User] = {}

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
    
    def addPlayer(self, player: User):
        del self.invited[player.id]
        self.players[player.id] = player
        msg = {"message": f"{player.username} accepted your invitation to your tournament", "refresh": ["/tournament/create/"]}
        sendMessageWS(self.organizer, "notifications", json.dumps(msg))

    def removePlayer(self, player: User):
        try: self.invited.pop(player.id)
        except: pass

        try: self.players.pop(player.id)
        except: pass

        if len(self.players) == 0:
            tournaments.pop(self.organizer.id)

    def userInvited(self, user: User) -> bool:
        return self.invited.get(user.id) != None
    
    def userJoined(self, user: User) -> bool:
        return self.players.get(user.id) != None

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
        if friend.status == "offline":
            friends.remove(friend)
        elif tournament.userInvited(friend) or tournament.userJoined(friend):
            friends.remove(friend)
    return render(request, "tournament/create.html",
        {"friends": friends, "ERROR": error, "SUCCESS": success, "players": tournament.players})