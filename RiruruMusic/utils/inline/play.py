import math

from config import SUPPORT_GROUP
from pyrogram.types import InlineKeyboardButton
from RiruruMusic.utils.formatters import time_to_seconds


## After Edits with Timer Bar

def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    mihir = math.floor(percentage)
    if 0 < mihir <= 10:
        bar = "◉—————————"
    elif 10 < mihir < 20:
        bar = "—◉————————"
    elif 20 <= mihir < 30:
        bar = "——◉———————"
    elif 30 <= mihir < 40:
        bar = "———◉——————"
    elif 40 <= mihir < 50:
        bar = "————◉—————"
    elif 50 <= mihir < 60:
        bar = "—————◉————"
    elif 60 <= mihir < 70:
        bar = "——————◉———"
    elif 70 <= mihir < 80:
        bar = "———————◉——"
    elif 80 <= mihir < 95:
        bar = "————————◉—"
    else:
        bar = "—————————◉"

    buttons = [
        [
            InlineKeyboardButton(text=f"{played} {bar} {dur}", callback_data="GetTimer")
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}")
        ],
        [
            InlineKeyboardButton(text="• sᴜᴩᴩᴏʀᴛ •", url=f"https://t.me/{SUPPORT_GROUP}"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
        ]
    ]
    return buttons


def telegram_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    mihir = math.floor(percentage)
    if 0 < mihir <= 10:
        bar = "◉—————————"
    elif 10 < mihir < 20:
        bar = "—◉————————"
    elif 20 <= mihir < 30:
        bar = "——◉———————"
    elif 30 <= mihir < 40:
        bar = "———◉——————"
    elif 40 <= mihir < 50:
        bar = "————◉—————"
    elif 50 <= mihir < 60:
        bar = "—————◉————"
    elif 60 <= mihir < 70:
        bar = "——————◉———"
    elif 70 <= mihir < 80:
        bar = "———————◉——"
    elif 80 <= mihir < 95:
        bar = "————————◉—"
    else:
        bar = "—————————◉"

    buttons = [
        [
            InlineKeyboardButton(text=f"{played} {bar} {dur}", callback_data="GetTimer")
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}")
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
        ],
    ]
    return buttons


def stream_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}")
        ],
        [
            InlineKeyboardButton(text="• sᴜᴩᴩᴏʀᴛ •", url=f"https://t.me/{SUPPORT_GROUP}"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
        ],
    ]
    return buttons


def telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
        ],
    ]
    return buttons


## Search Query Inline


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_1"], callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text=_["P_B_2"], callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {user_id}")
        ]
    ]
    return buttons

## Live Stream Markup

def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_3"], callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton(text=_["S_B_2"], url=f"https://t.me/{SUPPORT_GROUP}"),
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data=f"forceclose {user_id}")
        ]
    ]
    return buttons

def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_1"], callback_data=f"AltPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text=_["P_B_2"], callback_data=f"AltPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {user_id}")
        ]
    ]
    return buttons


## Slider Query Markup

def slider_markup(
    _, videoid, user_id, query, query_type, channel, fplay
):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(text=_["P_B_1"], callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"),
            InlineKeyboardButton(text=_["P_B_2"], callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}")
        ],
        [
            InlineKeyboardButton(text="◁", callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {user_id}"),
            InlineKeyboardButton(text="▷", callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}")
        ]
    ]
    return buttons


def botplaylist_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text="• sᴜᴩᴩᴏʀᴛ •", url=f"https://t.me/{SUPPORT_GROUP}"),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
        ]
    ]
    return buttons
