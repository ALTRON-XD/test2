import os
import re
import sys
import traceback
import subprocess

from time import time
from io import StringIO

from config import OWNER_ID
from RiruruMusic import app

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def aexec(code, client, message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@app.on_message(filters.command("eval") & filters.user(OWNER_ID) & ~filters.forwarded)
async def executor(client, message):
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.reply_text("**ᴡʜᴀᴛ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇxᴇᴄᴜᴛᴇ ?**")

    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    evaluation = evaluation.strip()

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="🗑 Close", callback_data=f"forceclose {message.from_user.id}"),
            ]
        ]
    )
    if len(evaluation) > 4000:
        filename = "COMPLETED.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(f"INPUT:\n\n{cmd}\n\n\nOUTPUT:\n\n{evaluation}")
        t2 = time()
        await message.reply_document(
            document=filename,
            caption=f"**OUTPUT:**\n`Attached Document`\n\n**TIME TAKEN:**\n{str(t2-t1)[:5]} Seconds",
            quote=False,
            reply_markup=keyboard,
        )
        os.remove(filename)
        await message.delete()
    else:
        t2 = time()
        final_output = f"**TIME TAKEN:**\n{str(t2-t1)[:5]} Seconds\n\n**OUTPUT**:\n`{evaluation}`"
        await message.reply_text(final_output, reply_markup=keyboard)


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    user_id = CallbackQuery.data.split(" ", 1)[1]
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("You're not allowed to close this.", show_alert=True)
        except:
            return
    await CallbackQuery.message.delete()


@app.on_message(filters.command("sh") & filters.user(OWNER_ID) & ~filters.forwarded)
async def shellrunner(client, message):
    if len(message.command) < 2:
        return await message.reply_text("**Example :**\n/sh git pull")

    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                await message.reply_text(f"**ERROR:**\n```{str(err)}```")
            output += f"**{code}**\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(exc_type, value=exc_obj, tb=exc_tb)
            return await message.reply_text(f"**ERROR:**\n```{''.join(errors)}```")
        output = process.stdout.read()[:-1].decode("utf-8")

    if str(output) == "\n":
        output = None

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="🗑 Close", callback_data=f"forceclose {message.from_user.id}"),
                ]
            ]
        )
    if output:
        if len(output) > 4000:
            with open("COMPLETED.txt", "w+") as file:
                file.write(output)
            await client.send_document(message.chat.id, "COMPLETED.txt", reply_to_message_id=message.id, caption="`Output`")
            return os.remove("COMPLETED.txt")
        await message.reply_text(f"**OUTPUT:**\n```{output}```", reply_markup=keyboard)
    else:
        await message.reply_text("**OUTPUT: **\n`No output`", reply_markup=keyboard)
