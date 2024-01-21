import sys
import config
import asyncio
import importlib

from config import BANNED_USERS

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

from RiruruMusic import LOGGER, app, userbot
from RiruruMusic.core.call import AltCall
from RiruruMusic.plugins import ALL_MODULES
from RiruruMusic.utils.database import get_banned_users, gbansdb


loop = asyncio.get_event_loop()


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("RiruruMusic").error("Atleast add a pyrogram string, Exiting...")
        return
    if (
        not config.SPOTIFY_CLIENT_ID
        and not config.SPOTIFY_CLIENT_SECRET
    ):
        LOGGER("RiruruMusic").warning("Fill SPOTIFY_CLIENT_ID & SPOTIFY_CLIENT_SECRET to play music from SPOTIFY")
    try:
        async for user in gbansdb.find({}):
            BANNED_USERS.add(user["_id"])
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("RiruruMusic.plugins." + all_module)
    LOGGER("RiruruMusic.plugins").info("Necessary Modules Imported Successfully.")
    await userbot.start()
    await AltCall.start()

    try:
        await AltCall.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("RiruruMusic").error("[ERROR] - \n\nPlease turn on your Logger Group's Voice Call. Make sure you never close/end voice call in your log group")
        sys.exit()
    except:
        pass
    await AltCall.decorators()
    LOGGER("RiruruMusic").info("Riruru Music Bot Started Successfully")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("RiruruMusic").info("Stopping Music Bot...")
