import os
import random
import asyncio
import time
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

from pyrogram import Client, filters, enums
from pyrogram.types import *
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from pyrogram.enums import ChatAction


# ============================================================
# ENV
# ============================================================

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise RuntimeError(
        "❌ MONGO_URL is missing. Add MONGO_URL to Heroku Config Vars."
    )


# ============================================================
# MONGODB
# ============================================================

try:
    mongo = MongoClient(
        MONGO_URL,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )

    # Force connection test
    mongo.admin.command("ping")

    print("✅ MongoDB connected successfully")

except Exception as e:
    raise RuntimeError(f"❌ MongoDB connection failed: {e}")


# ============================================================
# DATABASES / COLLECTIONS
# ============================================================

vickdb = mongo["VickDb"]["Vick"]
chatai = mongo["Word"]["WordDb"]


# ============================================================
# ADMIN CHECK
# ============================================================

async def is_admin(chat_id: int, user_id: int):

    try:
        async for member in BRANDEDCHAT.get_chat_members(
            chat_id,
            filter=enums.ChatMembersFilter.ADMINISTRATORS
        ):
            if member.user.id == user_id:
                return True

    except Exception as e:
        print(f"Admin check error: {e}")

    return False


# ============================================================
# CHATBOT ON
# ============================================================

@BRANDEDCHAT.on_message(
    filters.command("chatbot") & ~filters.private
)
async def chatbot_command(_, message: Message):

    if not message.from_user:
        return

    if not await is_admin(
        message.chat.id,
        message.from_user.id
    ):
        return await message.reply_text(
            "❌ You are not admin."
        )

    # Get argument
    if len(message.command) < 2:
        return await message.reply_text(
            "❌ Use:\n"
            "/chatbot on\n"
            "/chatbot off"
        )

    action = message.command[1].lower()

    # --------------------------------------------------------
    # ON
    # --------------------------------------------------------

    if action == "on":

        disabled = vickdb.find_one(
            {"chat_id": message.chat.id}
        )

        if not disabled:
            return await message.reply_text(
                "✅ Chatbot is already enabled."
            )

        vickdb.delete_one(
            {"chat_id": message.chat.id}
        )

        return await message.reply_text(
            "✅ Chatbot enabled."
        )

    # --------------------------------------------------------
    # OFF
    # --------------------------------------------------------

    elif action == "off":

        disabled = vickdb.find_one(
            {"chat_id": message.chat.id}
        )

        if disabled:
            return await message.reply_text(
                "⚠️ Chatbot is already disabled."
            )

        vickdb.insert_one(
            {
                "chat_id": message.chat.id,
                "disabled_at": datetime.utcnow(),
            }
        )

        return await message.reply_text(
            "🚫 Chatbot disabled."
        )

    else:

        return await message.reply_text(
            "❌ Invalid option.\n\n"
            "Use:\n"
            "/chatbot on\n"
            "/chatbot off"
        )


# ============================================================
# AI / WORD REPLY
# ============================================================

@BRANDEDCHAT.on_message(
    filters.text
    & ~filters.private
    & ~filters.bot
)
async def ai_text(_, message: Message):

    # Chatbot disabled
    if vickdb.find_one(
        {"chat_id": message.chat.id}
    ):
        return

    if not message.text:
        return

    data = list(
        chatai.find(
            {
                "word": message.text
            }
        )
    )

    if not data:
        return

    reply = random.choice(data)

    if reply.get("check") == "sticker":

        if reply.get("text"):
            try:
                await message.reply_sticker(
                    reply["text"]
                )
            except Exception as e:
                print(
                    f"Sticker reply error: {e}"
                )

    else:

        if reply.get("text"):
            await message.reply_text(
                reply["text"]
            )


# ============================================================
# START
# ============================================================

@BRANDEDCHAT.on_message(
    filters.command("start")
)
async def start(_, message: Message):

    await message.reply_photo(
        photo=START_IMG,
        caption=START,
        reply_markup=InlineKeyboardMarkup(MAIN)
    )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    print(f"{BOT_NAME} is alive")

    BRANDEDCHAT.run()
