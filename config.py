import re
import sys

from os import getenv
from pyrogram import filters
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID", "25981592"))
API_HASH = getenv("API_HASH", "709f3c9d34d83873d3c7e76cdd75b866")

BOT_TOKEN = getenv("BOT_TOKEN")

MONGO_DB_URI = getenv("MONGO_DB_URI")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "300"))

LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1001954218150"))

MUSIC_BOT_NAME = getenv("MUSIC_BOT_NAME", "Riruru Music")

OWNER_ID = int(getenv("OWNER_ID", "5980177243"))

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/TheRiruru/Riruru")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")

GIT_TOKEN = getenv("GIT_TOKEN", "" )

SUPPORT_GROUP = getenv("SUPPORT_GROUP", "AltronChats")
if SUPPORT_GROUP.startswith("@"):
    SUPPORT_GROUP = SUPPORT_GROUP[1:]
elif "t.me/" in SUPPORT_GROUP:
    try:
        SUPPORT_GROUP = SUPPORT_GROUP.split("t.me/")[1]
    except:
        SUPPORT_GROUP = "AltronChats"

AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "False")

AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "18000"))

AUTO_DOWNLOADS_CLEAR = getenv("AUTO_DOWNLOADS_CLEAR", "True")

YOUTUBE_DOWNLOAD_EDIT_SLEEP = int(getenv("YOUTUBE_EDIT_SLEEP", "5"))

TELEGRAM_DOWNLOAD_EDIT_SLEEP = int(getenv("TELEGRAM_EDIT_SLEEP", "6"))

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "")

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "50"))

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600"))

TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "1073741824"))
# https://www.gbmb.org/mb-to-bytes

STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)

BANNED_USERS = filters.user()
LOG = 2
DEV = 5980177243
LOG_FILE_NAME = "AltLogs.txt"

adminlist = {}
lyrical = {}
autoclean = []
db = {}

START_IMG_URL = getenv("START_IMG_URL", "https://te.legra.ph/file/938d91267eedec0f8da06.jpg")

PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://te.legra.ph/file/c5ae7505b832353b2dbfc.jpg")

STATS_IMG_URL = getenv("STATS_IMG_URL", "https://graph.org/file/2fe478bf983f4e9963c68.jpg")

TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://te.legra.ph/file/a44ac871100a1aabb360f.jpg")

TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://te.legra.ph/file/a44ac871100a1aabb360f.jpg")

STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://te.legra.ph/file/a44ac871100a1aabb360f.jpg")

YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://te.legra.ph/file/a44ac871100a1aabb360f.jpg")

SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://te.legra.ph/file/a44ac871100a1aabb360f.jpg")

SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://te.legra.ph/file/a44ac871100a1aabb360f.jpg")

SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://te.legra.ph/file/a44ac871100a1aabb360f.jpg")


def time_to_seconds(time):
    return sum(
        int(x) * 60**i
        for i, x in enumerate(reversed(str(time).split(":")))
    )

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if UPSTREAM_REPO:
    if not re.match("(?:http|https)://", UPSTREAM_REPO):
        print("[ERROR] - Your UPSTREAM_REPO url is wrong. Please ensure that it starts with https://")
        sys.exit()

if PLAYLIST_IMG_URL:
    if PLAYLIST_IMG_URL != "RiruruMusic/assets/Playlist.jpeg":
        if not re.match("(?:http|https)://", PLAYLIST_IMG_URL):
            print("[ERROR] - Your PLAYLIST_IMG_URL url is wrong. Please ensure that it starts with https://")
            sys.exit()

if STATS_IMG_URL:
    if STATS_IMG_URL != "RiruruMusic/assets/Stats.jpeg":
        if not re.match("(?:http|https)://", STATS_IMG_URL):
            print("[ERROR] - Your STATS_IMG_URL url is wrong. Please ensure that it starts with https://")
            sys.exit()


if TELEGRAM_AUDIO_URL:
    if TELEGRAM_AUDIO_URL != "RiruruMusic/assets/Audio.jpeg":
        if not re.match("(?:http|https)://", TELEGRAM_AUDIO_URL):
            print("[ERROR] - Your TELEGRAM_AUDIO_URL url is wrong. Please ensure that it starts with https://")
            sys.exit()


if STREAM_IMG_URL:
    if STREAM_IMG_URL != "RiruruMusic/assets/Stream.jpeg":
        if not re.match("(?:http|https)://", STREAM_IMG_URL):
            print("[ERROR] - Your STREAM_IMG_URL url is wrong. Please ensure that it starts with https://")
            sys.exit()

if YOUTUBE_IMG_URL:
    if YOUTUBE_IMG_URL != "RiruruMusic/assets/Youtube.jpeg":
        if not re.match("(?:http|https)://", YOUTUBE_IMG_URL):
            print("[ERROR] - Your YOUTUBE_IMG_URL url is wrong. Please ensure that it starts with https://")
            sys.exit()


if TELEGRAM_VIDEO_URL:
    if TELEGRAM_VIDEO_URL != "RiruruMusic/assets/Video.jpeg":
        if not re.match("(?:http|https)://", TELEGRAM_VIDEO_URL):
            print("[ERROR] - Your TELEGRAM_VIDEO_URL url is wrong. Please ensure that it starts with https://")
            sys.exit()


if not MUSIC_BOT_NAME.isascii():
    print("Please Do Not Use Fancy Font in Music Bot's Name!")
