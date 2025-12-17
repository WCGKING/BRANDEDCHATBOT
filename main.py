mongo = MongoClient(MONGO_URL)
vickdb = mongo["VickDb"]["Vick"]
chatai = mongo["Word"]["WordDb"]

async def is_admin(chat_id: int, user_id: int):
    async for member in BRANDEDCHAT.get_chat_members(
        chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):
        if member.user.id == user_id:
            return True
    return False

@BRANDEDCHAT.on_message(filters.command("chatbot on") & ~filters.private)
async def chatbot_on(_, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply_text("❌ You are not admin")

    if not vickdb.find_one({"chat_id": message.chat.id}):
        return await message.reply_text("✅ Chatbot already enabled")

    vickdb.delete_one({"chat_id": message.chat.id})
    await message.reply_text("✅ Chatbot enabled")

@BRANDEDCHAT.on_message(filters.command("chatbot off") & ~filters.private)
async def chatbot_off(_, message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply_text("❌ You are not admin")

    if vickdb.find_one({"chat_id": message.chat.id}):
        return await message.reply_text("⚠️ Chatbot already disabled")

    vickdb.insert_one({"chat_id": message.chat.id})
    await message.reply_text("🚫 Chatbot disabled")


@BRANDEDCHAT.on_message(filters.text & ~filters.private & ~filters.bot)
async def ai_text(_, message: Message):
    if vickdb.find_one({"chat_id": message.chat.id}):
        return

    data = list(chatai.find({"word": message.text}))
    if not data:
        return

    reply = random.choice(data)
    if reply.get("check") == "sticker":
        await message.reply_sticker(reply["text"])
    else:
        await message.reply_text(reply["text"])

# ❌ OLD (BROKEN)
toggle.insert_one(...)

# ✅ FIX
chatai.insert_one(...)


@BRANDEDCHAT.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_photo(
        photo=START_IMG,
        caption=START,
        reply_markup=InlineKeyboardMarkup(MAIN)
    )

if __name__ == "__main__":
    print(f"{BOT_NAME} is alive")
    BRANDEDCHAT.run()
