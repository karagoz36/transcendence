from . import auth
from . import index
from . import settings
from . import friends
from . import play
from . import profile

from .tournament import create as tournamentCreate
from .tournament import invite as tournamentInvite
from .tournament import join as tournamentJoin

from .pong import lobby

from .api.auth import login, logout, register

from .api.friends import addFriend, acceptFriend, removeFriend, sendMessage
