from config import LOG, LOG_GROUP_ID, MUSIC_BOT_NAME

from RiruruMusic import app
from RiruruMusic.utils.database import is_on_off


async def play_logs(message, streamtype):
    if await is_on_off(LOG):

        if message.chat.id != LOG_GROUP_ID:
            if message.chat.username:
                chatusername = f"@{message.chat.username}"
            else:
                chatusername = "ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
            logger_text = f"""**{MUSIC_BOT_NAME} ᴩʟᴀʏ ʟᴏɢɢᴇʀ**

**ᴄʜᴀᴛ:** {message.chat.title}
**ᴄʜᴀᴛ ɪᴅ:** `{message.chat.id}`
**ᴄʜᴀᴛ ʟɪɴᴋ:** {chatusername}

**ᴜsᴇʀ:** {message.from_user.mention}
**ᴜsᴇʀ ɪᴅ:** `{message.from_user.id}`
**ᴜsᴇʀɴᴀᴍᴇ:** @{message.from_user.username}

**sᴇᴀʀᴄʜᴇᴅ ғᴏʀ:** {message.text}

**sᴛʀᴇᴀᴍ ᴛʏᴩᴇ:** {streamtype}"""
            try:
                await app.send_message(LOG_GROUP_ID, text=logger_text, disable_web_page_preview=True)
            except:
                pass
        return
