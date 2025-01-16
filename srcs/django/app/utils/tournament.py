from transcendence.pages.tournament.create import tournaments
from django.contrib.auth.models import User
from enum import Enum

class e_UserTournamentStatus(Enum):
    NOT_INVITED = "not_invited"
    INVITED = "invited"
    JOINED = "joined"

class UserTournamentData:
    state = e_UserTournamentStatus.NOT_INVITED
    organizer: User

def getTournaments(user: User):
    userTournaments: list[UserTournamentData] = []

    for curr in tournaments.values():
        data = UserTournamentData()
        data.organizer = curr.organizer

        if curr.userInvited(user):
            data.state = e_UserTournamentStatus.INVITED
        elif curr.userJoined(user):
            data.state = e_UserTournamentStatus.JOINED

        if data.state != e_UserTournamentStatus.NOT_INVITED:
            userTournaments.append(data)
    return userTournaments