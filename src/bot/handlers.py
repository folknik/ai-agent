from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from settings.config import *
from database.postgres import db
from core.agent import run_agent
from settings.base import get_logger
from bot.utils import get_user_data
from parser.parser import get_content_from_url

logger = get_logger(__name__)

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    chat_id = message.chat.id
    user_id = message.from_user.id
    db.insert_chat_id(chat_id, user_id)
    logger.info(f"New user with user_id \'{user_id}\' request the bot from \'{chat_id}\' chat_id")
    await message.answer(f"Hello, I'm your AI assistant! I'll send you a summary of new Habr articles.")


@router.message()
async def echo_handler(message: Message) -> None:
    """
    Handler handle all message types
    """
    url = message.text
    logger.info(f"User with user_id \'{message.from_user.id}\' sent new url: \'{url}\'")
    if url.startswith("https:") or url.startswith("http:"):
        html_content = get_content_from_url(url=url)
        summary = run_agent(
            prompt=PROMPT_TEMPLATE,
            paragraph_count='3 обзацах',
            html_content=html_content
        )
        logger.info(f"AI agent summarized content: \n\'{summary}\'")
        user_data = get_user_data(message=message, url=url)
        db.insert_user_data(user_data=user_data)
        await message.answer(summary)
    else:
        logger.info(f"It was the bad url: \'{url}\'")
        await message.answer("Unfortunately, it was the bad url! Please, try again.")

