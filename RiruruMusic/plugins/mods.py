import os
import shutil
import dotenv
import asyncio
import urllib3

from strings import get_command
from config import OWNER_ID, LOG_FILE_NAME, UPSTREAM_BRANCH

from git import Repo
from pyrogram import filters
from datetime import datetime
from git.exc import GitCommandError, InvalidGitRepositoryError

from RiruruMusic import app
from RiruruMusic.misc import SUDOERS
from RiruruMusic.utils.pastebin import Altbin
from RiruruMusic.utils.decorators.language import language
from RiruruMusic.utils.database import get_active_chats, remove_active_chat, remove_active_video_chat


# Commands
GETLOG_COMMAND = get_command("GETLOG_COMMAND")
GETVAR_COMMAND = get_command("GETVAR_COMMAND")
DELVAR_COMMAND = get_command("DELVAR_COMMAND")
SETVAR_COMMAND = get_command("SETVAR_COMMAND")
UPDATE_COMMAND = get_command("UPDATE_COMMAND")
REBOOT_COMMAND = get_command("REBOOT_COMMAND")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@app.on_message(filters.command(GETLOG_COMMAND) & SUDOERS)
@language
async def log_(client, message, _):
    if os.path.exists(LOG_FILE_NAME):
        with open(LOG_FILE_NAME) as log:
            lines = log.readlines()
        data = ""
        try:
            NUMB = int(message.text.split(None, 1)[1])
        except:
            NUMB = 100
        for x in lines[-NUMB:]:
            data += x
        link = await Altbin(data)
        if link:
            return await message.reply_text(link)
        else:
            return await message.reply_document(LOG_FILE_NAME)
    else:
        return await message.reply_text(_["mods_2"].format(LOG_FILE_NAME))


@app.on_message(filters.command(GETVAR_COMMAND) & filters.user(OWNER_ID))
@language
async def varget_(client, message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["mods_3"])
    check_var = message.text.split(None, 2)[1]
    path = dotenv.find_dotenv()
    if not path:
        return await message.reply_text(_["mods_5"])
    output = dotenv.get_key(path, check_var)
    if not output:
        await message.reply_text(_["mods_4"])
    else:
        return await message.reply_text(f"**{check_var}:** `{str(output)}`")


@app.on_message(filters.command(DELVAR_COMMAND) & filters.user(OWNER_ID))
@language
async def vardel_(client, message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["mods_6"])
    check_var = message.text.split(None, 2)[1]
    path = dotenv.find_dotenv()
    if not path:
        return await message.reply_text(_["mods_5"])
    output = dotenv.unset_key(path, check_var)
    if not output[0]:
        return await message.reply_text(_["mods_4"])
    else:
        await message.reply_text(_["mods_7"].format(check_var))
        os.system(f"kill -9 {os.getpid()} && bash start")


@app.on_message(filters.command(SETVAR_COMMAND) & filters.user(OWNER_ID))
@language
async def set_var(client, message, _):
    if len(message.command) < 3:
        return await message.reply_text(_["mods_8"])
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    path = dotenv.find_dotenv()
    if not path:
        return await message.reply_text(_["mods_5"])
    dotenv.set_key(path, to_set, value)
    if dotenv.get_key(path, to_set):
        await message.reply_text(_["mods_9"].format(to_set))
    else:
        await message.reply_text(_["mods_10"].format(to_set))
    os.system(f"kill -9 {os.getpid()} && bash start")


@app.on_message(filters.command(UPDATE_COMMAND) & filters.user(OWNER_ID))
@language
async def update_(client, message, _):
    response = await message.reply_text(_["mods_13"])
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit_text(_["mods_11"])
    except InvalidGitRepositoryError:
        return await response.edit_text(_["mods_12"])

    os.system(f"git fetch origin {UPSTREAM_BRANCH} &> /dev/null")
    await asyncio.sleep(7)
    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]  # main git repository

    for checks in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        verification = str(checks.count())
    if verification == "":
        return await response.edit_text("ʙᴏᴛ ɪs ᴜᴩ-ᴛᴏ-ᴅᴀᴛᴇ ᴡɪᴛʜ ᴜᴩsᴛʀᴇᴀᴍ ʀᴇᴩᴏ !")
    updates = ""
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[
            (format // 10 % 10 != 1)
            * (format % 10 < 4)
            * format
            % 10 :: 4
        ],
    )
    for info in repo.iter_commits(f"HEAD..origin/{UPSTREAM_BRANCH}"):
        updates += f"<b>➣ #{info.count()}: [{info.summary}]({REPO_}/commit/{info}) by -> {info.author}</b>\n\t\t\t\t<b>➥ ᴄᴏᴍᴍɪᴛᴇᴅ ᴏɴ:</b> {ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} {datetime.fromtimestamp(info.committed_date).strftime('%b')}, {datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
    
    _update_response_ = "<b>ᴀ ɴᴇᴡ ᴜᴩᴅᴀᴛᴇ ɪs ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛʜᴇ ʙᴏᴛ !</b>\n\n➣ ᴩᴜsʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ɴᴏᴡ</code>\n\n**<u>ᴜᴩᴅᴀᴛᴇs:</u>**\n\n"
    _final_updates_ = _update_response_ + updates

    if len(_final_updates_) > 4096:
        url = await Altbin(_final_updates_)
        await response.edit_text(
            f"<b>ᴀ ɴᴇᴡ ᴜᴩᴅᴀᴛᴇ ɪs ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛʜᴇ ʙᴏᴛ !</b>\n\n➣ ᴩᴜsʜɪɴɢ ᴜᴩᴅᴀᴛᴇs ɴᴏᴡ</code>\n\n**<u>ᴜᴩᴅᴀᴛᴇs:</u>** [ᴄʜᴇᴄᴋ ᴜᴩᴅᴀᴛᴇs]({url})"
        )
    else:
        await response.edit_text(_final_updates_, disable_web_page_preview=True)

    os.system("git stash &> /dev/null && git pull")

    served_chats = await get_active_chats()
    for x in served_chats:
        await remove_active_chat(x)
        await remove_active_video_chat(x)
    await response.edit_text(f"{_final_updates_}ʙᴏᴛ ᴜᴩᴅᴀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ! ɴᴏᴡ ᴡᴀɪᴛ ғᴏʀ ғᴇᴡ ᴍɪɴᴜᴛᴇs ᴜɴᴛɪʟ ᴛʜᴇ ʙᴏᴛ ʀᴇsᴛᴀʀᴛs ᴀɴᴅ ᴩᴜsʜ ᴄʜᴀɴɢᴇs !")

    os.system("pip3 install -r requirements.txt")
    os.system(f"kill -9 {os.getpid()} && bash start")
    exit()


@app.on_message(filters.command(REBOOT_COMMAND) & filters.user(OWNER_ID))
async def reboot_(_, message):
    response = await message.reply_text("ʀᴇsᴛᴀʀᴛɪɴɢ...")
    served_chats = await get_active_chats()
    for x in served_chats:
        await remove_active_chat(x)
        await remove_active_video_chat(x)
    try:
        shutil.rmtree("downloads")
        shutil.rmtree("cache")
    except:
        pass
    await response.edit_text("ʀᴇsᴛᴀʀᴛ ᴩʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ, ᴡᴀɪᴛ ғᴏʀ ғᴇᴡ ᴍɪɴᴜᴛᴇs ᴜɴᴛɪʟ ᴛʜᴇ ʙᴏᴛ ʀᴇsᴛᴀʀᴛs.")
    os.system(f"kill -9 {os.getpid()} && bash start")
