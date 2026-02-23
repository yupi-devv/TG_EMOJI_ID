import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO, format="%(levelname)s|%(name)s|%(message)s")
logger = logging.getLogger(__name__)

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def hello(msg: Message):
    text = '<tg-emoji emoji-id="5440431182602842059">🫶</tg-emoji> <b>Привет, отправь мне любой кастомный эмодзи, а я пришлю тебе его id</b>'
    await msg.answer(text=text, parse_mode=ParseMode.HTML)


@dp.message()
async def handle_msg(msg: Message):
    if not msg.entities:
        return

    for entity in msg.entities:
        if entity.type != "custom_emoji":
            continue

        emoji_id = entity.custom_emoji_id

        text = (
            f"<b>Вот твой эмодзи:</b>\n\n"
            f"<b>✅ID:</b>\n"
            f"<code>{emoji_id}</code>\n\n"
            f"<b>✅HTML:</b>\n"
            f'<code>&lt;tg-emoji emoji-id="{emoji_id}"&gt;&lt;/tg-emoji&gt;</code>'
        )

        await msg.answer(text, parse_mode=ParseMode.HTML)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
