from asyncio import sleep

from config import OWNER_ID
from strings import get_command

from pyrogram import filters
from pyrogram.errors import FloodWait

from RiruruMusic import app
from RiruruMusic.utils.decorators.language import language
from RiruruMusic.utils.database import get_client, get_served_chats, get_served_users


BROADCAST_COMMAND = get_command("BROADCAST_COMMAND")
STOPBROADCAST_COMMAND = get_command("STOPBROADCAST_COMMAND")

IS_BROADCASTING = False

def is_broadcasting():
    return IS_BROADCASTING


@app.on_message(filters.command(BROADCAST_COMMAND) & filters.user(OWNER_ID))
@language
async def braodcast_message(client, message, _):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        return await message.reply_text(_["broad_8"])

    copy = False
    if message.reply_to_message:
        if message.text.startswith("/gcastx"):
            copy = True
            markup = message.reply_to_message.reply_markup
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        try:
            query = message.text.split(" ", 1)[1]
        except:
            return await message.reply_text(_["broad_5"])
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-assistant" in query:
            query = query.replace("-assistant", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await message.reply_text(_["broad_6"])

    IS_BROADCASTING = True

    # Bot broadcast inside chats
    if "-nobot" not in message.text:
        await message.reply_text(_["broad_9"])
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            if not IS_BROADCASTING:
                return
            if (sent % 300 == 0) and (sent > 0):
                await sleep(180)
            try:
                if copy:
                    m = await app.copy_message(i, y, x, reply_markup=markup)
                elif message.reply_to_message:
                    m = await app.forward_messages(i, y, x)
                else:
                    m = await app.send_message(i, text=query)
                sent += 1
                if "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except:
                        continue
                elif "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        continue
                await sleep(1)
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await sleep(flood_time)
            except:
                continue
        try:
            await message.reply_text(_["broad_1"].format(sent, pin))
        except:
            pass

    # Bot broadcasting to users
    if "-user" in message.text:
        await message.reply_text(_["broad_12"])
        susr = 0
        susers = await get_served_users()
        for user in susers:
            if not IS_BROADCASTING:
                return
            if (susr % 300 == 0) and (susr > 0):
                await sleep(180)
            try:
                if copy:
                    await app.copy_message(int(user["_id"]), y, x, reply_markup=markup)
                elif message.reply_to_message:
                    await app.forward_messages(int(user["_id"]), y, x)
                else:
                    await app.send_message(int(user["_id"]), text=query)
                susr += 1
                await sleep(1)
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await sleep(flood_time)
            except:
                pass
        try:
            await message.reply_text(_["broad_7"].format(susr))
        except:
            pass

    # Bot broadcasting by assistant
    if "-assistant" in message.text:
        await message.reply_text(_["broad_2"])
        text = _["broad_3"]
        from RiruruMusic.core.userbot import assistants

        for num in assistants:
            sent = 0
            client = await get_client(num)
            if not IS_BROADCASTING:
                return

            async for dialog in client.get_dialogs():
                if not IS_BROADCASTING:
                    return
                if (sent % 300 == 0) and (sent > 0):
                    await sleep(180)
                try:
                    if copy:
                        await client.copy_message(dialog.chat.id, y, x)
                    elif message.reply_to_message:
                        await client.forward_messages(dialog.chat.id, y, x)
                    else:
                        await client.send_message(dialog.chat.id, text=query)
                    sent += 1
                    await sleep(1)
                except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await sleep(flood_time)
                except:
                    continue
            text += _["broad_4"].format(num, sent)
        try:
            await message.reply_text(text)
        except:
            pass
    IS_BROADCASTING = False


@app.on_message(filters.command(STOPBROADCAST_COMMAND) & filters.user(OWNER_ID))
@language
async def stopbraodcast_message(client, message, _):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        IS_BROADCASTING = False
        await message.reply_text(_["broad_11"])
    else:
        await message.reply_text(_["broad_10"])
