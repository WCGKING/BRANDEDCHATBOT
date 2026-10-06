import os
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient

from pyrogram import Client, filters, enums
from pyrogram.types import Message


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# ENVIRONMENT VARIABLES
# ============================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
MONGO_URL = os.getenv("MONGO_URL")


# ============================================================
# CHECK REQUIRED VARIABLES
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
# MONGODB CONNECTION
# ============================================================

try:

    mongo = MongoClient(
        MONGO_URL,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
        socketTimeoutMS=10000,
        maxPoolSize=50,
        minPoolSize=5,
        retryWrites=True,
    )

    mongo.admin.command("ping")

    print("✅ MongoDB connected successfully")

except Exception as e:

    raise RuntimeError(
        f"❌ MongoDB connection failed: {e}"
    )


# ============================================================
# DATABASE / COLLECTIONS
# ============================================================

vickdb = mongo[
    "VickDb"
][
    "Vick"
]

chatai = mongo[
    "Word"
][
    "WordDb"
]


# ============================================================
# DATABASE INDEXES
# ============================================================
#
# Existing indexes:
#
# chat_id_1
# word_1_autocreated
#
# No manual create_index() is required.
#
# ============================================================

print("✅ Using existing MongoDB indexes")


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

    if not message.from_user:
        return

    # --------------------------------------------------------
    # ADMIN CHECK
    # --------------------------------------------------------

    if not await is_admin(
        message.chat.id,
        message.from_user.id
    ):

        return await message.reply_text(
            "❌ You must be an admin to use this command."
        )

    # --------------------------------------------------------
    # ARGUMENT CHECK
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
    # ENABLE CHATBOT
    # ========================================================

    if action == "on":

        disabled = vickdb.find_one(
            {
                "chat_id": chat_id
            },
            {
                "_id": 1
            }
        )

        if not disabled:

            return await message.reply_text(
                "✅ Chatbot is already enabled."
            )

        vickdb.delete_one(
            {
                "chat_id": chat_id
            }
        )

        return await message.reply_text(
            "✅ Chatbot enabled successfully."
        )

    # ========================================================
    # DISABLE CHATBOT
    # ========================================================

    if action == "off":

        disabled = vickdb.find_one(
            {
                "chat_id": chat_id
            },
            {
                "_id": 1
            }
        )

        if disabled:

            return await message.reply_text(
                "⚠️ Chatbot is already disabled."
            )

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
    # INVALID OPTION
    # ========================================================

    return await message.reply_text(
        "❌ Invalid option.\n\n"
        "Use:\n"
        "/chatbot on\n"
        "/chatbot off"
    )


# ============================================================
# FAST CHATBOT REPLY
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

    if not message.text:
        return

    chat_id = message.chat.id
    user_text = message.text.strip()

    if not user_text:
        return

    # --------------------------------------------------------
    # CHECK CHATBOT STATUS
    # --------------------------------------------------------

    disabled = vickdb.find_one(
        {
            "chat_id": chat_id
        },
        {
            "_id": 1
        }
    )

    if disabled:
        return

    # ========================================================
    # FIND RANDOM REPLY
    # ========================================================

    try:

        result = next(
            chatai.aggregate(
                [
                    {
                        "$match": {
                            "word": user_text
                        }
                    },
                    {
                        "$sample": {
                            "size": 1
                        }
                    }
                ],
                allowDiskUse=False,
            ),
            None
        )

    except Exception as e:

        print(
            f"❌ MongoDB reply error: {e}"
        )

        return

    if not result:
        return

    # --------------------------------------------------------
    # GET REPLY
    # --------------------------------------------------------

    reply_text = result.get(
        "text"
    )

    reply_type = result.get(
        "check"
    )

    if not reply_text:
        return

    # ========================================================
    # STICKER REPLY
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
    # TEXT REPLY
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
# PING COMMAND
# ============================================================

@BRANDEDCHAT.on_message(
    filters.command("ping")
)
async def ping(
    _,
    message: Message
):

    await message.reply_text(
        "🤖 <b>Bot is working.</b>"
    )


# ============================================================
# START BOT
# ============================================================

if __name__ == "__main__":

    print(
        "=============================================="
    )

    print(
        "🚀 Vick Bot is starting..."
    )

    print(
        "✅ MongoDB connected"
    )

    print(
        "✅ Pyrogram client initialized"
    )

    print(
        "=============================================="
    )

    BRANDEDCHAT.run()

