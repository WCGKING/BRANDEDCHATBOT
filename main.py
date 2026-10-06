import os
import random
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

BOT_NAME = os.getenv(
    "BOT_NAME",
    "Vick Bot"
)

START_IMG = os.getenv(
    "START_IMG",
    ""
)


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

    # Test connection
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

try:

    # Only create chat_id index.
    #
    # IMPORTANT:
    # Do NOT create an index on "word".
    #
    # Your MongoDB already has:
    #
    # word_1_autocreated
    #
    # Creating another "word" index causes:
    #
    # IndexOptionsConflict / code 85
    #

    vickdb.create_index(
        [("chat_id", 1)],
        unique=True,
        name="chat_id_unique",
    )

    print(
        "✅ MongoDB indexes ready"
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
    # USER CHECK
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # BASIC CHECK
    # --------------------------------------------------------

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
    # FIND REPLY
    # ========================================================
    #
    # IMPORTANT:
    #
    # We are NOT doing:
    #
    # list(chatai.find(...))
    #
    # because that loads every matching reply into RAM.
    #
    # Instead MongoDB itself selects one random document.
    #
    # This is faster and better for large collections.
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
# START COMMAND
# ============================================================

@BRANDEDCHAT.on_message(
    filters.command("start")
)
async def start(
    _,
    message: Message
):

    user = (
        message.from_user.mention
        if message.from_user
        else "there"
    )


    text = (
        f"👋 Hello {user}!\n\n"
        f"🤖 <b>{BOT_NAME}</b> is online.\n\n"
        "Use <code>/chatbot on</code> or "
        "<code>/chatbot off</code> in groups."
    )


    # --------------------------------------------------------
    # START IMAGE
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
    # TEXT FALLBACK
    # --------------------------------------------------------

    await message.reply_text(
        text
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
        "🏓 <b>Pong!</b>\n"
        "✅ Bot is working."
    )


# ============================================================
# START BOT
# ============================================================

if __name__ == "__main__":

    print(
        "=============================================="
    )

    print(
        f"🚀 {BOT_NAME} is starting..."
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
