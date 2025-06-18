from typing import Tuple
from aiogram import Bot
from aiogram.types import Message

from database.postgres import db
from core.agent import run_agent
from settings.logger import get_logger
from prompts.summary_agent_prompt import PROMPT_TEMPLATE
from parsers.habr_parser import get_content_from_url, get_articles_from_last_day


logger = get_logger(__name__)


async def send_new_articles(bot: Bot) -> None:
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
                summary = run_agent(
                    prompt=PROMPT_TEMPLATE,
                    paragraph_count='1 обзаце',
                    html_content=html_content
                )
                message = f"<a href='{article['link']}'>{article['name']}</a>" + "\n\n" + summary
                db.insert_article(
                    name=article['name'],
                    link=article['link'],
                    published_datetime=article['dt']
                )
                for chat in chats:
                    await bot.send_message(chat_id=chat, text=message)
        else:
            logger.info("There are no new articles")
    else:
        logger.info("There is no chat in database")


def get_user_data(message: Message, url: str) -> Tuple:
    return (
        message.from_user.id,
        message.chat.id,
        message.from_user.is_bot,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username,
        message.from_user.is_premium,
        url
    )
