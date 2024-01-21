import asyncio

from strings import get_string
from config import MUSIC_BOT_NAME, PLAYLIST_IMG_URL, adminlist

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import (
    ChatAdminRequired, UserAlreadyParticipant, UserNotParticipant, PeerIdInvalid, InviteRequestSent
)

from RiruruMusic import YouTube, app
from RiruruMusic.misc import SUDOERS
from RiruruMusic.utils.inline.play import botplaylist_markup
from RiruruMusic.utils.database.memorydatabase import is_maintenance
from RiruruMusic.utils.database.assistantdatabase import get_assistant
from RiruruMusic.utils.database import get_cmode, get_lang, get_playmode, get_playtype, is_active_chat


def PlayWrapper(command):
    async def wrapper(client, message):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    "» ʙᴏᴛ ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ғᴏʀ sᴏᴍᴇ ᴛɪᴍᴇ, ᴩʟᴇᴀsᴇ ᴠɪsɪᴛ [sᴜᴩᴩᴏʀᴛ ᴄʜᴀᴛ](https://t.me/AltronChats) ᴛᴏ ᴋɴᴏᴡ ᴛʜᴇ ʀᴇᴀsᴏɴ..."
                )
        try:
            await message.delete()
        except:
            pass
        language = await get_lang(message.chat.id)
        _ = get_string(language)
        audio_telegram = (
            (
                message.reply_to_message.audio
                or message.reply_to_message.voice
            )
            if message.reply_to_message
            else None
        )
        video_telegram = (
            (
                message.reply_to_message.video
                or message.reply_to_message.document
            )
            if message.reply_to_message
            else None
        )
        url = await YouTube.url(message)
        if (
            audio_telegram is None
            and video_telegram is None
            and url is None
        ):
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text(_["str_1"])
                buttons = botplaylist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["playlist_1"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="How to fix this ?", callback_data="AnonymousAdmin")
                    ]
                ]
            )
            return await message.reply_text(_["general_4"], reply_markup=upl)
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_12"])
            try:
                chat = await app.get_chat(chat_id)
            except:
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None
        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await message.reply_text(_["admin_18"])
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text(_["play_4"])
        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None
        if message.command[0][-1] == "e":
            if not await is_active_chat(chat_id):
                return await message.reply_text(_["play_18"])
            fplay = True
        else:
            fplay = None
        if not await is_active_chat(chat_id):
            userbot = await get_assistant(chat_id)
            try:
                get = await app.get_chat_member(chat_id, userbot.id)
                
                if get.status == ChatMemberStatus.BANNED or get.status == ChatMemberStatus.LEFT:
                    upl = InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(text=f"ᴜɴʙᴀɴ {userbot.name}", callback_data=f"unban_assistant {chat_id}|{userbot.id}")
                            ]
                        ]
                    )
                    return await message.reply_text(_["call_2"].format(MUSIC_BOT_NAME, userbot.name, userbot.id, userbot.username), reply_markup=upl)
            except ChatAdminRequired:
                return await message.reply_text(_["call_1"])
            except UserNotParticipant:
                chat = await app.get_chat(chat_id)
                if chat.username:
                    try:
                        await userbot.join_chat(chat.username)
                    except UserAlreadyParticipant:
                        pass
                    except InviteRequestSent:
                        return await message.reply_text(_["call_13"].format(userbot.name))
                    except Exception as e:
                        return await message.reply_text(_["call_3"].format(e))
                else:
                    try:
                        invitelink = chat.invite_link
                        if not invitelink:
                            invitelink = await app.export_chat_invite_link(chat_id)
                    except ChatAdminRequired:
                        return await message.reply_text(_["call_1"])
                    except Exception as e:
                        return await message.reply_text(_["call_3"].format(e))
                    try:
                        m = await app.send_message(chat_id, _["call_4"].format(userbot.name, chat.title))
                        if invitelink.startswith("https://t.me/+"):
                            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                        await asyncio.sleep(1)
                        await userbot.join_chat(invitelink)
                        await m.edit_text(_["call_5"].format(MUSIC_BOT_NAME))
                    except UserAlreadyParticipant:
                        pass
                    except InviteRequestSent:
                        return await message.reply_text(_["call_13"].format(userbot.name))
                    except Exception as e:
                        return await message.reply_text(_["call_3"].format(e))
            except PeerIdInvalid:
                button = InlineKeyboardMarkup([[InlineKeyboardButton("• ᴄʟɪᴄᴋ ᴛᴏ ᴠᴇʀɪғʏ •", url=f"https://t.me/{app.username}")]])
                return await message.reply_text(_["call_12"], reply_markup=button)

        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
