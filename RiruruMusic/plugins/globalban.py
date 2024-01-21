import asyncio

from strings import get_command
from config import BANNED_USERS, OWNER_ID

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from RiruruMusic import app
from RiruruMusic.misc import SUDOERS
from RiruruMusic.utils import get_readable_time
from RiruruMusic.utils.decorators.language import language
from RiruruMusic.utils.database import get_served_chats, gbansdb


# Commands
GBAN_COMMAND = get_command("GBAN_COMMAND")
UNGBAN_COMMAND = get_command("UNGBAN_COMMAND")
GBANNED_COMMAND = get_command("GBANNED_COMMAND")


@app.on_message(filters.command(GBAN_COMMAND) & filters.user(OWNER_ID))
@language
async def gbanuser(client, message: Message, _):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.mention
    else:
        try:
            user = message.text.split(None, 1)[1]
            user = await app.get_users(user)
        except:
            return await message.reply_text(_["general_1"])
        user_id = user.id
        mention = user.mention

    if user_id == message.from_user.id:
        return await message.reply_text(_["gban_1"])
    elif user_id == app.id:
        return await message.reply_text(_["gban_2"])
    elif user_id in SUDOERS:
        return await message.reply_text(_["gban_3"])
    is_gbanned = await gbansdb.find_one({"_id": user_id})
    if is_gbanned:
        return await message.reply_text(_["gban_4"].format(mention))
    if user_id not in BANNED_USERS:
        BANNED_USERS.add(user_id)
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = len(served_chats)
    time_expected = get_readable_time(time_expected)
    mystic = await message.reply_text(_["gban_5"].format(mention, time_expected))
    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await app.ban_chat_member(chat_id, user_id)
            number_of_chats += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception:
            pass
    await gbansdb.insert_one({"_id": user_id})
    await message.reply_text(_["gban_6"].format(mention, number_of_chats))
    await mystic.delete()


@app.on_message(filters.command(UNGBAN_COMMAND) & filters.user(OWNER_ID))
@language
async def gungabn(client, message: Message, _):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.mention
    else:
        try:
            user = message.text.split(None, 1)[1]
            user = await app.get_users(user)
        except:
            return await message.reply_text(_["general_1"])
        user_id = user.id
        mention = user.mention

    is_gbanned = await gbansdb.find_one({"_id": user_id})
    if not is_gbanned:
        return await message.reply_text(_["gban_7"].format(mention))
    if user_id in BANNED_USERS:
        BANNED_USERS.remove(user_id)
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = len(served_chats)
    time_expected = get_readable_time(time_expected)
    mystic = await message.reply_text(_["gban_8"].format(mention, time_expected))
    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await app.unban_chat_member(chat_id, user_id)
            number_of_chats += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception:
            pass
    await gbansdb.delete_one({"_id": user_id})
    await message.reply_text(_["gban_9"].format(mention, number_of_chats))
    await mystic.delete()


@app.on_message(filters.command(GBANNED_COMMAND) & filters.user(OWNER_ID))
@language
async def gbanned_list(client, message: Message, _):
    mystic = await message.reply_text(_["gban_11"])

    msg = "ɢʙᴀɴɴᴇᴅ ᴜsᴇʀs:\n\n"
    count = 0

    async for user in gbansdb.find({}):
        count += 1
        try:
            userx = await app.get_users(user["_id"])
            msg += f"{count}➤ {userx.mention}\n"
        except Exception:
            msg += f'{count}➤ [ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ]{user["_id"]}\n'

    if count == 0:
        await mystic.edit_text(_["gban_10"])
    else:
        await mystic.edit_text(msg)
