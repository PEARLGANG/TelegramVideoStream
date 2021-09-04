from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from player.stream import app

bot = Client(
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="player"),
)
Bot = Client(
        "bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        workers=2
    )
Bot.start()
app.start()
idle()
