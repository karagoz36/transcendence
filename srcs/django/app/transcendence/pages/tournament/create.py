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
    players: list[User] = []
    invited: list[User] = []
    
    def __init__(self, organizer: User):
        self.organizer = organizer
    
    async def inviteUser(self, invited: User):
        self.invited.append(invited)
        msg = json.dumps({"message": f"<a href='/tournament/join/?id={self.organizer.id}'>{self.organizer.username} invited you to its tournament</a>"})
        await sendMessageWS(invited, "notifications", msg)
    
    def addPlayer(self, player: User):
        self.invited.remove(player)
        self.players.append(player)

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
        tournaments[user.id] = Tournament(user)
    
    if tournament:
        for friend in friends:
            if friend in tournament.invited or friend.status == "offline":
                friends.remove(friend)
    return render(request, "tournament/create.html",
        {"friends": friends, "ERROR": error, "SUCCESS": success})