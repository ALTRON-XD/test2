from aiohttp import ClientSession

from RiruruMusic.logging import LOGGER

from RiruruMusic.misc import sudo
from RiruruMusic.core.git import git
from RiruruMusic.core.dir import dirr
from RiruruMusic.core.bot import MusicBot
from RiruruMusic.core.userbot import Userbot


dirr()

git()

sudo()

# Clients
app = MusicBot()

userbot = Userbot()


from RiruruMusic.platforms import *

YouTube = YouTubeAPI()
Carbon = CarbonAPI()
Spotify = SpotifyAPI()
Telegram = TeleAPI()

aiohttpsession = ClientSession()
