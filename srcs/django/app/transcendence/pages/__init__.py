from . import auth
from . import index
from . import settings
from . import friends
from . import play
from . import profile
from . import profile_list
from . import update_settings


from .pong import lobby

from .api.auth import login, logout, register

from .api.friends import addFriend, acceptFriend, removeFriend, sendMessage, openMessage
