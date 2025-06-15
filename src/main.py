import asyncio
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode

from langchain_openai import OpenAI
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from settings.config import *
from settings.base import get_logger
from settings.telegram import get_user_data
from database.postgres import PostgresDB
from utils.data import get_content_from_url, get_articles_from_last_day

logger = get_logger(__name__)

scheduler = AsyncIOScheduler(timezone="UTC")
bot = Bot(token=TOKEN)

llm = OpenAI(
    model=LLM_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=LLM_TEMPERATURE,
    max_tokens=LLM_MAX_TOKENS,
    max_retries=LLM_MAX_RETRIES
)

db = PostgresDB()

dp = Dispatcher()


def run_agent(html_content: str) -> str:
    inputs = [
        {
            "role": "system",
            "content": PROMPT_TEMPLATE.format(html_content=html_content)
        }
    ]
    response = llm.invoke(inputs)
    return response


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    db.insert_chat_id(chat_id, user_id)
    logger.info(f"New user with user_id \'{user_id}\' request the bot from \'{chat_id}\' chat_id")
    await message.answer(f"Hello, I'm your AI assistant! Send me a link to the article and I'll send you a summary.")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler handle all message types
    """
    url = message.text
    logger.info(f"User with user_id \'{message.from_user.id}\' sent new url: \'{url}\'")
    if url.startswith("https:") or url.startswith("http:"):
        html_content = get_content_from_url(url=url)
        summary = run_agent(html_content=html_content)
        logger.info(f"AI agent summarized content: \n\'{summary}\'")
        user_data = get_user_data(message=message, url=url)
        db.insert_user_data(user_data=user_data)
        await message.answer(summary)
    else:
        logger.info(f"It was the bad url: \'{url}\'")
        await message.answer("Unfortunately, it was the bad url! Please, try again.")


async def collect_habr_content():
    chats = db.get_all_chats()
    if len(chats) > 0:
        articles = get_articles_from_last_day()
        message = ''
        for article in articles:
            html_content = get_content_from_url(url=article['link'])
            summary = run_agent(html_content=html_content)
            message += f"<a href='{article['link']}'>{article['name']}</a>" + "\n" + summary
        for chat in chats:
            await bot.send_message(chat_id=chat, text=message, parse_mode=ParseMode.HTML)
    else:
        logger.info("There is no chat in database")


# Run the bot
async def main() -> None:
    logger.info(f"Telegram bot started...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    scheduler.add_job(
        func=collect_habr_content,
        trigger=CronTrigger.from_crontab("30 6 * * *")
    )
    scheduler.start()
    asyncio.run(main())
