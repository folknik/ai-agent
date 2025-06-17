from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode

from settings.config import *
from database.postgres import db
from core.agent import run_agent
from settings.base import get_logger
from settings.telegram import get_user_data
from utils.data import get_content_from_url, get_articles_from_last_day


logger = get_logger(__name__)


bot = Bot(token=TOKEN)
dp = Dispatcher()


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
        summary = run_agent(prompt=PROMPT_TEMPLATE, html_content=html_content)
        logger.info(f"AI agent summarized content: \n\'{summary}\'")
        user_data = get_user_data(message=message, url=url)
        db.insert_user_data(user_data=user_data)
        await message.answer(summary)
    else:
        logger.info(f"It was the bad url: \'{url}\'")
        await message.answer("Unfortunately, it was the bad url! Please, try again.")


async def collect_habr_content():
    chats = db.get_all_chats()
    chats = [chat[0] for chat in chats]
    logger.info(f'Available chat list: {chats}')
    if len(chats) > 0:
        articles = get_articles_from_last_day()
        links_to_article = db.get_all_links_to_article()
        links_to_article = [link[0] for link in links_to_article]
        filtered_articles = [art for art in articles if art['link'] not in links_to_article]
        if len(filtered_articles) > 0:
            for article in filtered_articles:
                html_content = get_content_from_url(url=article['link'])
                summary = run_agent(prompt=HABR_PROMPT_TEMPLATE, html_content=html_content)
                message = f"<a href='{article['link']}'>{article['name']}</a>" + "\n\n" + summary
                db.insert_article(
                    name=article['name'],
                    link=article['link'],
                    published_datetime=article['dt']
                )
                for chat in chats:
                    await bot.send_message(chat_id=chat, text=message, parse_mode=ParseMode.HTML)
        else:
            logger.info("There are no new articles")
    else:
        logger.info("There is no chat in database")
