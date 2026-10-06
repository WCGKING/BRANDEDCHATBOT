import os
import random
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

from pyrogram import Client, filters, enums
from pyrogram.types import Message


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
MONGO_URL = os.getenv("MONGO_URL")

BOT_NAME = os.getenv("BOT_NAME", "Vick Bot")
START_IMG = os.getenv("START_IMG", "")


# ============================================================
# ENVIRONMENT VALIDATION
# ============================================================

missing = []

if not BOT_TOKEN:
    missing.append("BOT_TOKEN")

if not API_ID:
    missing.append("API_ID")

if not API_HASH:
    missing.append("API_HASH")

if not MONGO_URL:
    missing.append("MONGO_URL")

if missing:
    raise RuntimeError(
        "❌ Missing environment variables: "
        + ", ".join(missing)
    )


# ============================================================
# PYROGRAM CLIENT
# ============================================================

BRANDEDCHAT = Client(
    "VickBot",
    api_id=int(API_ID),
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)


# ============================================================
# MONGODB
# ============================================================

try:
    mongo = MongoClient(
        MONGO_URL,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
    )

    # Test MongoDB connection
    mongo.admin.command("ping")

    print("✅ MongoDB connected successfully")

except Exception as e:
    raise RuntimeError(
        f"❌ MongoDB connection failed: {e}"
    )


# ============================================================
# DATABASE / COLLECTIONS
# ============================================================

vickdb = mongo["VickDb"]["Vick"]
chatai = mongo["Word"]["WordDb"]


# ============================================================
# DATABASE INDEXES
# ============================================================

try:
    vickdb.create_index(
        "chat_id",
        unique=True
    )

    chatai.create_index(
        "word"
    )

except Exception as e:
    print(
        f"⚠️ MongoDB index warning: {e}"
    )


# ============================================================
# ADMIN CHECK
# ============================================================

async def is_admin(
    chat_id: int,
    user_id: int
) -> bool:

    try:

        member = await BRANDEDCHAT.get_chat_member(
            chat_id,
            user_id
        )

        return member.status in (
            enums.ChatMemberStatus.OWNER,
            enums.ChatMemberStatus.ADMINISTRATOR,
        )

    except Exception as e:

        print(
            f"❌ Admin check error: {e}"
        )

        return False


# ============================================================
# CHATBOT ON / OFF
# ============================================================

@BRANDEDCHAT.on_message(
    filters.command("chatbot")
    & ~filters.private
)
async def chatbot_command(
    _,
    message: Message
):

    # --------------------------------------------------------
    # User check
    # --------------------------------------------------------

    if not message.from_user:
        return

    # --------------------------------------------------------
    # Admin check
    # --------------------------------------------------------

    if not await is_admin(
        message.chat.id,
        message.from_user.id
    ):

        return await message.reply_text(
            "❌ You must be an admin to use this command."
        )

    # --------------------------------------------------------
    # Argument check
    # --------------------------------------------------------

    if len(message.command) < 2:

        return await message.reply_text(
            "❌ Invalid command.\n\n"
            "Use:\n"
            "/chatbot on\n"
            "/chatbot off"
        )

    action = message.command[1].lower()

    chat_id = message.chat.id

    # ========================================================
    # CHATBOT ON
    # ========================================================

    if action == "on":

        disabled = vickdb.find_one(
            {
                "chat_id": chat_id
            }
        )

        # Already enabled
        if not disabled:

            return await message.reply_text(
                "✅ Chatbot is already enabled."
            )

        # Remove disabled record
        vickdb.delete_one(
            {
                "chat_id": chat_id
            }
        )

        return await message.reply_text(
            "✅ Chatbot enabled successfully."
        )

    # ========================================================
    # CHATBOT OFF
    # ========================================================

    if action == "off":

        disabled = vickdb.find_one(
            {
                "chat_id": chat_id
            }
        )

        # Already disabled
        if disabled:

            return await message.reply_text(
                "⚠️ Chatbot is already disabled."
            )

        # Save disabled chat
        vickdb.insert_one(
            {
                "chat_id": chat_id,
                "disabled_at": datetime.utcnow(),
            }
        )

        return await message.reply_text(
            "🚫 Chatbot disabled successfully."
        )

    # ========================================================
    # INVALID ACTION
    # ========================================================

    return await message.reply_text(
        "❌ Invalid option.\n\n"
        "Use:\n"
        "/chatbot on\n"
        "/chatbot off"
    )


# ============================================================
# CHATBOT WORD REPLY
# ============================================================

@BRANDEDCHAT.on_message(
    filters.text
    & ~filters.private
    & ~filters.bot
)
async def ai_text(
    _,
    message: Message
):

    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    if not message.text:
        return

    chat_id = message.chat.id

    # --------------------------------------------------------
    # Check whether chatbot is disabled
    # --------------------------------------------------------

    disabled = vickdb.find_one(
        {
            "chat_id": chat_id
        }
    )

    if disabled:
        return

    # --------------------------------------------------------
    # Find matching word
    # --------------------------------------------------------

    data = list(
        chatai.find(
            {
                "word": message.text
            }
        )
    )

    if not data:
        return

    # --------------------------------------------------------
    # Random reply
    # --------------------------------------------------------

    reply = random.choice(data)

    reply_text = reply.get("text")
    reply_type = reply.get("check")

    if not reply_text:
        return

    # ========================================================
    # STICKER
    # ========================================================

    if reply_type == "sticker":

        try:

            await message.reply_sticker(
                reply_text
            )

        except Exception as e:

            print(
                f"❌ Sticker reply error: {e}"
            )

        return

    # ========================================================
    # NORMAL TEXT
    # ========================================================

    try:

        await message.reply_text(
            reply_text
        )

    except Exception as e:

        print(
            f"❌ Text reply error: {e}"
        )


# ============================================================
# START COMMAND
# ============================================================

@BRANDEDCHAT.on_message(
    filters.command("start")
)
async def start(
    _,
    message: Message
):

    text = (
        f"👋 Hello {message.from_user.mention if message.from_user else 'there'}!\n\n"
        f"🤖 {BOT_NAME} is online."
    )

    # --------------------------------------------------------
    # Send start image if configured
    # --------------------------------------------------------

    if START_IMG:

        try:

            await message.reply_photo(
                photo=START_IMG,
                caption=text,
            )

            return

        except Exception as e:

            print(
                f"⚠️ START_IMG error: {e}"
            )

    # --------------------------------------------------------
    # Fallback text
    # --------------------------------------------------------

    await message.reply_text(
        text
    )


# ============================================================
# ERROR HANDLER
# ============================================================

@BRANDEDCHAT.on_message(
    filters.command("ping")
)
async def ping(
    _,
    message: Message
):

    await message.reply_text(
        "🏓 Pong!\n"
        "✅ Bot is working."
    )


# ============================================================
# START BOT
# ============================================================

if __name__ == "__main__":

    print("=" * 50)
    print(f"🚀 {BOT_NAME} is starting...")
    print("✅ MongoDB connected")
    print("✅ Pyrogram client initialized")
    print("=" * 50)

    BRANDEDCHAT.run()
