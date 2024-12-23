from . import auth
from . import index
from . import settings
from . import friends
from . import play

from .api.auth import login
from .api.auth import logout
from .api.auth import register
from .api.auth import register

from .api.friends import addFriend
from .api.friends import acceptFriend
from .api.friends import removeFriend
from .api.friends import sendMessage

from .api.play import sendGameInvite