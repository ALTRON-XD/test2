from strings import get_command
from config import LOG, LOG_GROUP_ID

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from RiruruMusic import app
from RiruruMusic.misc import SUDOERS
from RiruruMusic.utils.database import add_off, add_on
from RiruruMusic.utils.decorators.language import language


LOGGER_COMMAND = get_command("LOGGER_COMMAND")


@app.on_message(filters.command(LOGGER_COMMAND) & SUDOERS)
@language
async def logger(client, message, _):
    usage = _["log_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await add_on(LOG)
        await message.reply_text(_["log_2"])
    elif state == "disable":
        await add_off(LOG)
        await message.reply_text(_["log_3"])
    else:
        await message.reply_text(usage)


@app.on_message(filters.left_chat_member, group=2)
async def on_left_chat_member(client: Client, message: Message):
    if message.left_chat_member.is_self:
        remove_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        text = f"**✫** <b><u>ʟᴇғᴛ ɢʀᴏᴜᴘ</u></b> **:**\n\n**ᴄʜᴀᴛ ɪᴅ :** `{message.chat.id}`\n**ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ** : @{message.chat.username}\n**ᴄʜᴀᴛ ᴛɪᴛʟᴇ :** {message.chat.title}\n\n**ʀᴇᴍᴏᴠᴇᴅ ʙʏ :** {remove_by}"
        reply_markup = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(message.from_user.first_name, user_id=message.from_user.id)
            ]
        ])
        await client.send_message(LOG_GROUP_ID, text, reply_markup=reply_markup)
