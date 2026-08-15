import os
import asyncio
from telegram import Bot

TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

async def send():
    bot = Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="Bot chal gaya ✅")

asyncio.run(send())
