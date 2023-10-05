#Don't remove This Line From Here. @BRANDEDKING82| @BRANDRD_BOT 
#Github :- WCGKING | @BRANDED_WORLD 
import requests
import random
import os
import re
import asyncio
import time
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import *

from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli


API_ID = os.environ.get("API_ID","") 
API_HASH = os.environ.get("API_HASH","") 
BOT_TOKEN = os.environ.get("BOT_TOKEN","") 
MONGO_URL = os.environ.get("MONGO_URL","mongodb+srv://Musicbot58:93529352@cluster0.n6wscri.mongodb.net/?retryWrites=true&w=majority")
BOT_USERNAME = os.environ.get("Khushi_chat_bot") 
UPDATE_CHNL = os.environ.get("https://t.me/BRANDRD_BOT")
OWNER_ID = os.environ.get("6258877205")
OWNER_USERNAME = os.environ.get("BRANDEDKING82")
SUPPORT_GRP = os.environ.get("https://t.me/BRANDED_WORLD")
BOT_NAME = os.environ.get("≛⃝𝐌𝐈𝐒𝐒 🇰𝐡𝐮𝐬𝐡𝐢 𓆩 𝐃𝐑𝐀𝐌𝐀 🇶𝗨𝗘𝗘𝗡๛🖤")
START_IMG1 = os.environ.get("https://telegra.ph/file/b27a946b7dd4a89dcb205.jpg")
START_IMG2 = os.environ.get("https://graph.org/file/70c214a03ad0b53d239e0.jpg")
START_IMG3 = os.environ.get("https://telegra.ph/file/3fd4025a4f9864b7819f0.jpg")
START_IMG4 = os.environ.get("https://telegra.ph/file/6db1c486e1266eb1991f1.jpg")
START_IMG5 = os.environ.get("https://telegra.ph/file/4f26ff4ad7bd6a7a6c9f2.jpg")
START_IMG6 = os.environ.get("")
START_IMG7 = os.environ.get("https://telegra.ph/file/4f26ff4ad7bd6a7a6c9f2.jpg")
START_IMG8 = os.environ.get("https://telegra.ph/file/4f26ff4ad7bd6a7a6c9f2.jpg")
START_IMG9 = os.environ.get("https://telegra.ph/file/6db1c486e1266eb1991f1.jpg")
START_IMG10 = os.environ.get("https://graph.org/file/178a27531b99dfeffd70b.jpg")
STKR = os.environ.get("STKR", "CAACAgUAAxkBAAIrmGPowSnK3r_vRdbF4XIGlMH96JFWAAKIBQACJIpZVFm_q-vw2ClpLgQ")
STKR1 = os.environ.get("STKR1", "CAACAgUAAxkBAAIrkWPowR2DK8uD3MtiJrvSxDGUuOGhAAIrBQACgJ5YVOetqbdOj2DXLgQ")
STKR2 = os.environ.get("STKR2", "CAACAgUAAxkBAAIrk2PowSDe18eYXmSUL3O6Nz8ywhYWAALsBwACbDxhVNPtqf8K-NtbLgQ")
STKR3 = os.environ.get("STKR3", "CAACAgUAAxkBAAIrlGPowSFNEfC8mbKmn9JaqnEZAnGZAAL4BwACH1BZVM9gYnj0gjP3LgQ")
STKR4 = os.environ.get("STKR4", "CAACAgUAAxkBAAIrlWPowSKZtNGqkqAl9sqhuWcJ72WvAAJCBgACckSIVOdYxiec-Sa9LgQ")
STKR5 = os.environ.get("STKR5", "CAACAgUAAxkBAAIrlWPowSKZtNGqkqAl9sqhuWcJ72WvAAJCBgACckSIVOdYxiec-Sa9LgQ")
STKR6 = os.environ.get("STKR6", "CAACAgUAAxkBAAIrlmPowSj3u8c6iGJH5OM43bWqiI8oAAKBBQACLSBZVGrX0D_CrKlBLgQ")
STKR7 = os.environ.get("STKR7", "CAACAgUAAxkBAAIrl2PowSnMnL_gUifRw_NHlx6FYVLbAALvAwACJstYVPgI-6FGciajLgQ")
STKR8 = os.environ.get("STKR8", "CAACAgUAAxkBAAIrmGPowSnK3r_vRdbF4XIGlMH96JFWAAKIBQACJIpZVFm_q-vw2ClpLgQ")

bot = Client(
    "VickBot" ,
    api_id = API_ID,
    api_hash = API_HASH ,
    bot_token = BOT_TOKEN
)

mongo = MongoCli(MONGO_URL)
db = mongo.Anonymous
chatsdb = db.chatsdb
usersdb = db.users

async def is_admins(chat_id: int):
    return [
        member.user.id
        async for member in bot.iter_chat_members(
            chat_id, filter="administrators"
        )
    ]


PHOTO = [
    START_IMG1,
    START_IMG2,
    START_IMG3,
    START_IMG4,
    START_IMG5,
    START_IMG6,
    START_IMG7,
    START_IMG8,
    START_IMG9,
    START_IMG10,
]

EMOJIOS = [ 
      "💣",
      "💥",
      "🪄",
      "🧨",
      "⚡",
      "🤡",
      "👻",
      "🎃",
      "🎩",
      "🕊",
]
      
STICKER = [
      STKR,
      STKR1,
      STKR2,
      STKR3,
      STKR4,
      STKR5,
      STKR6,
      STKR7,
      STKR8,
]
START = f"""
**๏ ʜᴇʏ, ɪ ᴀᴍ [{BOT_NAME}]({START_IMG1})**
**ᴊɪsᴋᴇ ᴊᴀɪʙ ᴍᴇ ɢᴀɴᴅʜɪ  ᴄʜᴏʀɪ ᴜsᴋᴇ ᴘʏᴀᴀʀ ᴍᴇ ᴀᴀɴᴅʜɪ 🖤**
**──────────────**
**➻ ᴜsᴀɢᴇ /chatbot [ᴏɴ/ᴏғғ]**
<b>||๏ 𝐀𝐊𝐄𝐋𝐄 𝐊𝐇𝐀𝐃𝐄 𝐇𝐎𝐍𝐄 𝐊𝐀 𝐒𝐀𝐇𝐀𝐒 𝐑𝐀𝐊𝐇𝐎 𝐂𝐇𝐀𝐇𝐄 𝐏𝐔𝐑𝐈 𝐊𝐀𝐘𝐍𝐀𝐓 𝐀𝐀𝐏𝐊𝐄 𝐊𝐇𝐈𝐋𝐀𝐅 𝐊𝐇𝐀𝐃𝐈 𝐇𝐎 🚬🦋🖤🔥.||</b>
"""
DEV_OP = [
    [
        InlineKeyboardButton(text="🚩 ᴏᴡɴᴇʀ 🚩", url=f"t.me/{OWNER_USERNAME}"),
        InlineKeyboardButton(text="🚩ꜱᴜᴘᴘᴏʀᴛ 🚩", url=f"https://t.me/{SUPPORT_GRP}"),
    ],
    [
        InlineKeyboardButton(
            text="🚩 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ 🚩",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="🚩 ʜᴇʟᴘ & ᴄᴍᴅs 🚩", callback_data="HELP"),
    ],
    [
        InlineKeyboardButton(text="🚩 sᴏᴜʀᴄᴇ 🚩", callback_data="SOURCE"),
        InlineKeyboardButton(text="🚩 ᴀʙᴏᴜᴛ 🚩", callback_data="ABOUT"),
    ],
]
PNG_BTN = [
    [
         InlineKeyboardButton(
             text="🚩 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ 🚩",
             url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
         ),
     ],
     [
         InlineKeyboardButton(
             text="🚩 sᴜᴘᴘᴏʀᴛ 🚩", 
             url=f"https://t.me/{SUPPORT_GRP}",
         ),
     ],
]
HELP_READ = f"""
<u>**ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ {BOT_NAME}**</u>
<u>**ᴀʀᴇ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ!**</u>
**ᴀʟʟ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ:/**
**──────────────**

"""
BACK = [
     [
           InlineKeyboardButton(text="🚩 ʙᴀᴄᴋ 🚩", callback_data="BACK"),
     ],
]
HELP_BTN = [
     [
          InlineKeyboardButton(text="🚩 ᴄʜᴀᴛʙᴏᴛ 🚩", callback_data="CHATBOT_CMD"),
          InlineKeyboardButton(text="🚩 ᴛᴏᴏʟs 🚩", callback_data="TOOLS_DATA"),
     ],
     [
          InlineKeyboardButton(text="🚩 ʙᴀᴄᴋ 🚩", callback_data="BACK"),
          InlineKeyboardButton(text="🚩 ᴄʟᴏsᴇ 🚩", callback_data="CLOSE"),
     ],
]

CLOSE_BTN = [
      [
           InlineKeyboardButton(text="🚩 ᴄʟᴏsᴇ 🚩", callback_data="CLOSE"),
      ],
]

CHATBOT_ON = [
        [
            InlineKeyboardButton(text="ᴇɴᴀʙʟᴇ", callback_data=f"addchat"),
            InlineKeyboardButton(text="ᴅɪsᴀʙʟᴇ", callback_data=f"rmchat"),
        ],
]

PNG_BTN = [
    [
         InlineKeyboardButton(
             text="🚩 ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ 🧸",
             url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
         ),
     ],
     [
         InlineKeyboardButton(text="🚩 ᴄʟᴏsᴇ 🚩", 
                              callback_data="CLOSE",
         ),
     ],
]

TOOLS_DATA_READ = f"""
<u>**ᴛᴏᴏʟs ғᴏʀ {BOT_NAME} ᴀʀᴇ:**</u>
**➻ ᴜsᴇ `/repo` ғᴏʀ ɢᴇᴛᴛɪɴɢ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ!**
**──────────────**
**➻ ᴜsᴇ `/ping` ғᴏʀ ᴄʜᴇᴄᴋɪɴɢ ᴛʜᴇ ᴘɪɴɢ ᴏғ {BOT_NAME}**
**──────────────**

"""

async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list

async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})

async def get_served_chats() -> list:
    chats = chatsdb.find({"chat_id": {"$lt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=1000000000):
        chats_list.append(chat)
    return chats_list

async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})

CHATBOT_READ = f"""
<u>**ᴄᴏᴍᴍᴀɴᴅs ғᴏʀ {BOT_NAME}**</u>
**➻ ᴜsᴇ `/chatbot` ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴛʜᴇ ᴄʜᴀᴛʙᴏᴛ.**
**๏ ɴᴏᴛᴇ ➻ ᴛʜᴇ ᴀʙᴏᴠᴇ ᴄᴏᴍᴍᴀɴᴅ ғᴏʀ ᴄʜᴀᴛʙᴏᴛ ᴡᴏʀᴋ ɪɴ ɢʀᴏᴜᴘ ᴏɴʟʏ!!**
**───────────────**

"""
CHATBOT_BACK = [
        [     
              InlineKeyboardButton(text="✨ ʙᴀᴄᴋ ✨", callback_data="CHATBOT_BACK"),
              InlineKeyboardButton(text="❄️ ᴄʟᴏsᴇ ❄️", callback_data="CLOSE"),
        ],
]
HELP_START = [
     [
            InlineKeyboardButton(text="🚀 ʜᴇʟᴘ 🚀", callback_data="HELP"),
            InlineKeyboardButton(text="🐳 ᴄʟᴏsᴇ 🐳", callback_data="CLOSE"),
     ],
]

HELP_BUTN = [
     [
           InlineKeyboardButton(text="🚀 ʜᴇʟᴘ 🚀", url=f"https://t.me/{BOT_USERNAME}?start=help"),
           InlineKeyboardButton(text="🐳 ᴄʟᴏsᴇ 🐳", callback_data="CLOSE"),
     ],
]

ABOUT_BTN = [
      [
           InlineKeyboardButton(text="🎄 sᴜᴘᴘᴏʀᴛ 🎄", url=f"https://t.me/{SUPPORT_GRP}"),  
           InlineKeyboardButton(text="🚀 ʜᴇʟᴘ 🚀", callback_data="HELP"),
      ],
      [    
           InlineKeyboardButton(text="🍾 ᴏᴡɴᴇʀ 🍾", url=f"https://t.me/{OWNER_USERNAME}"), 
           InlineKeyboardButton(text="❄️ sᴏᴜʀᴄᴇ ❄️", callback_data="SOURCE"),
      ],
      [ 
           InlineKeyboardButton(text="🐳 ᴜᴘᴅᴀᴛᴇs 🐳", url=f"https://t.me/{UPDATE_CHNL}"),  
           InlineKeyboardButton(text="✨ ʙᴀᴄᴋ ✨", callback_data="BACK"),
      ],
]
SOURCE_READ = f"**ʜᴇʏ, ᴛʜᴇ sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ᴏғ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ɪs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ.**\n**ᴘʟᴇᴀsᴇ ғᴏʀᴋ ᴛʜᴇ ʀᴇᴘᴏ & ɢɪᴠᴇ ᴛʜᴇ sᴛᴀʀ ✯**\n**──────────────────**\n**ʜᴇʀᴇ ɪs ᴛʜᴇ [sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ](https://telegra.ph/file/4f26ff4ad7bd6a7a6c9f2.jpg)**\n**──────────────────**\n**ɪғ ʏᴏᴜ ғᴀᴄᴇ ᴀɴʏ ᴘʀᴏʙʟᴇᴍ ᴛʜᴇɴ ᴄᴏɴᴛᴀᴄᴛ ᴀᴛ [sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ](https://t.me/{SUPPORT_GRP}).\n<b>||"

ABOUT_READ = f"""
**➻ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ɪs ᴀɴ ᴀɪ ʙᴀsᴇᴅ ᴄʜᴀᴛ-ʙᴏᴛ.**
**➻ [{BOT_NAME}](https://t.me/{BOT_USERNAME}) ʀᴇᴘʟɪᴇs ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.**
**➻ ʜᴇʟᴘs ʏᴏᴜ ɪɴ ᴀᴄᴛɪᴠᴀᴛɪɴɢ ʏᴏᴜʀ ɢʀᴏᴜᴘs.**
**➻ ᴡʀɪᴛᴛᴇɴ ɪɴ [ᴘʏᴛʜᴏɴ](https://www.python.org) ᴡɪᴛʜ [ᴍᴏɴɢᴏ-ᴅʙ](https://www.mongodb.com) ᴀs ᴀ ᴅᴀᴛᴀʙᴀsᴇ**
**──────────────**
**➻ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʙᴀsɪᴄ ʜᴇʟᴩ ᴀɴᴅ ɪɴғᴏ ᴀʙᴏᴜᴛ [{BOT_NAME}](https://t.me/{BOT_USERNAME})**
"""
@bot.on_message(filters.command(["start", "aistart", f"start@{BOT_USERNAME}"]))
async def restart(client, m: Message):
    if m.chat.type == "private":
        accha = await m.reply_text(
            text = random.choice(EMOJIOS),
        )
        await asyncio.sleep(1.3)
        await accha.edit("__ᴅιиg ᴅσиg ꨄ︎ ѕтαятιиg..__")
        await asyncio.sleep(0.2)
        await accha.edit("__ᴅιиg ᴅσиg ꨄ sтαятιиg.....__")
        await asyncio.sleep(0.2)
        await accha.edit("__ᴅιиg ᴅσиg ꨄ︎ sтαятιиg..__")
        await asyncio.sleep(0.2)
        await accha.delete()
        umm = await m.reply_sticker(sticker=random.choice(STICKER))
        await asyncio.sleep(2)
        await umm.delete()
        await m.reply_photo(
            photo = random.choice(PHOTO),
            caption=f"""**๏ ʜᴇʏ, ɪ ᴀᴍ [{BOT_NAME}](t.me/{BOT_USERNAME})**\n**➻ ᴀɴ ᴀɪ ʙᴀsᴇᴅ ᴄʜᴀᴛʙᴏᴛ.**\n**──────────────**\n**➻ ᴜsᴀɢᴇ /chatbot [ᴏɴ/ᴏғғ]**\n<b>||๏ ʜɪᴛ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ʜᴇʟᴘ||</b>""",
            reply_markup=InlineKeyboardMarkup(DEV_OP),
        )
        await add_served_user(m.from_user.id)
    else:
        await m.reply_photo(
            photo=random.choice(PHOTO),
            caption=START,
            reply_markup=InlineKeyboardMarkup(HELP_START),
        )
        await add_served_chat(m.chat.id)

@bot.on_callback_query()
async def cb_handler(Client, query: CallbackQuery):
    vickdb = MongoClient(MONGO_URL)
    vick = vickdb["VickDb"]["Vick"]
    if query.data == "HELP":
        await query.message.edit_text(
                      text = HELP_READ,
                      reply_markup=InlineKeyboardMarkup(HELP_BTN),
                      disable_web_page_preview=True,
     )
    elif query.data == "CLOSE":
            await query.message.delete()
    elif query.data == "BACK":
            await query.message.edit(
                  text = START,
                  reply_markup=InlineKeyboardMarkup(DEV_OP),
     )
    elif query.data == "SOURCE":
            await query.message.edit(
                   text = SOURCE_READ,
                   reply_markup = InlineKeyboardMarkup(BACK),
                   disable_web_page_preview = True,

     )
    elif query.data == "ABOUT":
            await query.message.edit(
                    text = ABOUT_READ,
                    reply_markup = InlineKeyboardMarkup(ABOUT_BTN),
                    disable_web_page_preview=True,
     )
    elif query.data == "ADMINS":
            await query.message.edit(
                    text = ADMIN_READ,
                    reply_markup = InlineKeyboardMarkup(MUSIC_BACK_BTN), 
     )
    elif query.data== "TOOLS_DATA":
            await query.message.edit(
                    text= TOOLS_DATA_READ,
                    reply_markup = InlineKeyboardMarkup(CHATBOT_BACK),
     )
    elif query.data == "BACK_HELP":
            await query.message.edit(
                    text = HELP_READ,
                    reply_markup = InlineKeyboardMarkup(HELP_BTN),
     )
    elif query.data == "CHATBOT_CMD":
            await query.message.edit(
                    text = CHATBOT_READ,
                    reply_markup = InlineKeyboardMarkup(CHATBOT_BACK), 
     )
    elif query.data == "CHATBOT_BACK":
            await query.message.edit(
                    text = HELP_READ,
                    reply_markup = InlineKeyboardMarkup(HELP_BTN), 
     )
    elif query.data == "addchat":
        if query.from_user.id not in (await is_admins(query.message.chat.id)):
            return query.answer(
                "You don't have permissions to do this baby.",
                show_alert=True,
            )
        else:
            is_vick = vick.find_one({"chat_id": query.message.chat.id})
            if not is_vick:           
                await query.edit_message_text(f"**ᴄʜᴀᴛ-ʙᴏᴛ ᴀʟʀᴇᴀᴅʏ ᴇɴᴀʙʟᴇᴅ.**")
            if is_vick:
                vick.delete_one({"chat_id": query.message.chat.id})
                await query.edit_message_text(f"**ᴄʜᴀᴛ-ʙᴏᴛ ᴇɴᴀʙʟᴇᴅ ʙʏ** {query.from_user.mention}.")
    elif query.data == "rmchat":
        if query.from_user.id not in (await is_admins(query.message.chat.id)):
            return query.answer(
                "**ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍs ᴛᴏ ᴅᴏ ᴛʜɪs ʙᴀʙʏ!**",
                show_alert=True,
            )
        else:
            is_vick = vick.find_one({"chat_id": query.message.chat.id})
            if not is_vick:
                vick.insert_one({"chat_id": query.message.chat.id})
                await query.edit_message_text(f"**ᴄʜᴀᴛ-ʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ ʙʏ** {query.from_user.mention}.")
            if is_vick:
                await query.edit_message_text("**ᴄʜᴀᴛ-ʙᴏᴛ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ.**")
                            
@bot.on_message(filters.command("repo"))
async def repo(client, message):
    await message.reply_text(
       text=SOURCE_READ,
       reply_markup=InlineKeyboardMarkup(CLOSE_BTN),
       disable_web_page_preview=True,
    )

@bot.on_message(filters.command(["help", f"help@{BOT_USERNAME}"], prefixes=["+", ".", "/", "-", "?", "$"]))
async def restart(client, m: Message):
    if m.chat.type == "private":
        hmm = await m.reply_photo(
            photo=random.choice(PHOTO),
            caption=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )
        await add_served_user(m.from_user.id)
    else:
        await m.reply_photo(
            photo=random.choice(PHOTO),
            caption="**ʜᴇʏ, ᴘᴍ ᴍᴇ ғᴏʀ ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs!**",
            reply_markup=InlineKeyboardMarkup(HELP_BUTN),
        )
        await add_served_chat(m.chat.id)


@bot.on_message(filters.command("stats"))
async def get_st(_, msg: Message):
    users = len(await get_served_users())
    chats = len(await get_served_chats())
    await msg.reply_photo(photo="https://te.legra.ph/file/2d5b054acddf865d4d83e.png",
                          caption=f"""ᴛᴏᴛᴀʟ sᴛᴀᴛs ᴏғ {BOT_NAME}
          ➻ **ᴄʜᴀᴛs :** {chats}
          ➻ **ᴜsᴇʀs :** {users}"""
    )

@bot.on_message(filters.command("ping", prefixes=["+", "/", "-", "?", "$", "&"]))
async def ping(client, message: Message):
    if message.chat.type == "private":
        await add_served_user(message.from_user.id)
    else:
        await add_served_chat(message.chat.id)
    await message.delete()
    start = datetime.now()
    wtfbhemchomd = await message.reply_sticker(sticker= random.choice(STICKER))
    ms = (datetime.now()-start).microseconds / 1000
    await message.reply_photo(
        photo=random.choice(PHOTO),
        caption=f"нey вαву!!\n**[{BOT_NAME}](t.me/{BOT_USERNAME})** ιѕ alιve 🥀 αnd worĸιng ғιne wιтн a pιng oғ\n➥ `{ms}` ms\n\n<b>||мαdє ωιтн ❣️ ву [Developer](https://t.me/{OWNER_USERNAME})||</b>",
        reply_markup=InlineKeyboardMarkup(PNG_BTN),
    )

                  
@bot.on_message(
    filters.command(["chatbot", f"chatbot@{BOT_USERNAME}"])
    & ~filters.private)
async def chatonoff(client: Client, message: Message):
    if not message.from_user:
        return
    else:
        user = message.from_user.id
        chat_id = message.chat.id
        if user not in (await is_admins(chat_id)):
            return await message.reply_text(
                "**ʏᴏᴜ ᴀʀᴇ'ɴᴛ ᴀɴ ᴀᴅᴍɪɴ.**"
            )
        else:
            await message.reply_text(
            text="» <u>**ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**</u>",
            reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
        )


@bot.on_message(
 (
        filters.text
        | filters.sticker
    )
    & ~filters.private
    & ~filters.bot,
)
async def vickai(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]   

   if not message.reply_to_message:
       vickdb = MongoClient(MONGO_URL)
       vick = vickdb["VickDb"]["Vick"] 
       is_vick = vick.find_one({"chat_id": message.chat.id})
       if not is_vick:
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.text})  
           k = chatai.find_one({"word": message.text})      
           if k:               
               for x in is_chat:
                   K.append(x['text'])          
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
               if Yo == "sticker":
                   await message.reply_sticker(f"{hey}")
               if not Yo == "sticker":
                   await message.reply_text(f"{hey}")
   
   if message.reply_to_message:  
       vickdb = MongoClient(MONGO_URL)
       vick = vickdb["VickDb"]["Vick"] 
       is_vick = vick.find_one({"chat_id": message.chat.id})    
       getme = await bot.get_me()
       bot_id = getme.id                             
       if message.reply_to_message.from_user.id == bot_id: 
           if not is_vick:                   
               await bot.send_chat_action(message.chat.id, "typing")
               K = []  
               is_chat = chatai.find({"word": message.text})
               k = chatai.find_one({"word": message.text})      
               if k:       
                   for x in is_chat:
                       K.append(x['text'])
                   hey = random.choice(K)
                   is_text = chatai.find_one({"text": hey})
                   Yo = is_text['check']
                   if Yo == "sticker":
                       await message.reply_sticker(f"{hey}")
                   if not Yo == "sticker":
                       await message.reply_text(f"{hey}")
       if not message.reply_to_message.from_user.id == bot_id:          
           if message.sticker:
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.sticker.file_id, "check": "sticker", "id": message.sticker.file_unique_id})
           if message.text:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.text, "text": message.text})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})    
               

@bot.on_message(
 (
        filters.sticker
        | filters.text
    )
    & ~filters.private
    & ~filters.bot,
)
async def vickstickerai(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]   

   if not message.reply_to_message:
       vickdb = MongoClient(MONGO_URL)
       vick = vickdb["VickDb"]["Vick"] 
       is_vick = vick.find_one({"chat_id": message.chat.id})
       if not is_vick:
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.sticker.file_unique_id})      
           k = chatai.find_one({"word": message.text})      
           if k:           
               for x in is_chat:
                   K.append(x['text'])
               hey = random.choice(K)
               is_text = chatai.find_one({"text": hey})
               Yo = is_text['check']
               if Yo == "text":
                   await message.reply_text(f"{hey}")
               if not Yo == "text":
                   await message.reply_sticker(f"{hey}")
   
   if message.reply_to_message:
       vickdb = MongoClient(MONGO_URL)
       vick = vickdb["VickDb"]["Vick"] 
       is_vick = vick.find_one({"chat_id": message.chat.id})
       getme = await bot.get_me()
       bot_id = getme.id
       if message.reply_to_message.from_user.id == bot_id: 
           if not is_vick:                    
               await bot.send_chat_action(message.chat.id, "typing")
               K = []  
               is_chat = chatai.find({"word": message.text})
               k = chatai.find_one({"word": message.text})      
               if k:           
                   for x in is_chat:
                       K.append(x['text'])
                   hey = random.choice(K)
                   is_text = chatai.find_one({"text": hey})
                   Yo = is_text['check']
                   if Yo == "text":
                       await message.reply_text(f"{hey}")
                   if not Yo == "text":
                       await message.reply_sticker(f"{hey}")
       if not message.reply_to_message.from_user.id == bot_id:          
           if message.text:
               is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text})
               if not is_chat:
                   toggle.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.text, "check": "text"})
           if message.sticker:                 
               is_chat = chatai.find_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id})                 
               if not is_chat:
                   chatai.insert_one({"word": message.reply_to_message.sticker.file_unique_id, "text": message.sticker.file_id, "check": "none"})    
               


@bot.on_message(
    (
        filters.text
        | filters.sticker
    )
    & filters.private
    & ~filters.bot,
)
async def vickprivate(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"]
   if not message.reply_to_message: 
       await bot.send_chat_action(message.chat.id, "typing")
       K = []  
       is_chat = chatai.find({"word": message.text})                 
       for x in is_chat:
           K.append(x['text'])
       hey = random.choice(K)
       is_text = chatai.find_one({"text": hey})
       Yo = is_text['check']
       if Yo == "sticker":
           await message.reply_sticker(f"{hey}")
       if not Yo == "sticker":
           await message.reply_text(f"{hey}")
   if message.reply_to_message:            
       getme = await bot.get_me()
       bot_id = getme.id       
       if message.reply_to_message.from_user.id == bot_id:                    
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.text})                 
           for x in is_chat:
               K.append(x['text'])
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
           if Yo == "sticker":
               await message.reply_sticker(f"{hey}")
           if not Yo == "sticker":
               await message.reply_text(f"{hey}")
       

@bot.on_message(
 (
        filters.sticker
        | filters.text
    )
    & filters.private
    & ~filters.bot,
)
async def vickprivatesticker(client: Client, message: Message):

   chatdb = MongoClient(MONGO_URL)
   chatai = chatdb["Word"]["WordDb"] 
   if not message.reply_to_message:
       await bot.send_chat_action(message.chat.id, "typing")
       K = []  
       is_chat = chatai.find({"word": message.sticker.file_unique_id})                 
       for x in is_chat:
           K.append(x['text'])
       hey = random.choice(K)
       is_text = chatai.find_one({"text": hey})
       Yo = is_text['check']
       if Yo == "text":
           await message.reply_text(f"{hey}")
       if not Yo == "text":
           await message.reply_sticker(f"{hey}")
   if message.reply_to_message:            
       getme = await bot.get_me()
       bot_id = getme.id       
       if message.reply_to_message.from_user.id == bot_id:                    
           await bot.send_chat_action(message.chat.id, "typing")
           K = []  
           is_chat = chatai.find({"word": message.sticker.file_unique_id})                 
           for x in is_chat:
               K.append(x['text'])
           hey = random.choice(K)
           is_text = chatai.find_one({"text": hey})
           Yo = is_text['check']
           if Yo == "text":
               await message.reply_text(f"{hey}")
           if not Yo == "text":
               await message.reply_sticker(f"{hey}")

print(f"{BOT_NAME} ɪs ᴀʟɪᴠᴇ! ɴᴏᴡ ғᴜᴄᴋ ᴏғғ! ᴀɴᴅ ɢᴏ ᴛᴏ @Wᴇ_ʀғʀɪᴇɴᴅs ʙɪᴛᴄʜ!!")      
bot.run()
