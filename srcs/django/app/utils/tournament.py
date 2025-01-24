from transcendence.pages.tournament.create import tournaments
from django.contrib.auth.models import User
from enum import Enum

class e_UserTournamentStatus(Enum):
    UNREGISTERED = "unregistered"
    REGISTERED = "registed"

class UserTournamentData:
    state = e_UserTournamentStatus.UNREGISTERED
    organizer: User

def getTournaments(user: User):
    userTournaments: list[UserTournamentData] = []

    for curr in tournaments.values():
        if curr.organizer == user or curr.started:
            continue
        data = UserTournamentData()
        data.organizer = curr.organizer
        data.state = e_UserTournamentStatus.UNREGISTERED

        if curr.userJoined(user):
            data.state = e_UserTournamentStatus.REGISTERED
        userTournaments.append(data)
    return userTournaments