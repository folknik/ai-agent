import asyncio
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from langchain_openai import OpenAI

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

from settings.config import *
from utils.base import get_logger


logger = get_logger(__name__)


llm = OpenAI(
    model=LLM_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=LLM_TEMPERATURE,
    max_tokens=LLM_MAX_TOKENS,
    max_retries=LLM_MAX_RETRIES
)


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


def get_summary_from_url(url: str) -> str:
    req = Request(url, headers=HEADERS)
    with urlopen(req) as response:
        html = BeautifulSoup(response.read(), 'html.parser')
        html_content = html.get_text()
    summary = run_agent(html_content=html_content)
    return summary


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, I'm your AI assistant! Send me a link to the article and I'll send you a summary.")


@dp.message()
async def echo_handler(message: Message) -> None:
    """
    Handler handle all message types
    """
    url = message.text
    user_id = message.from_user.id
    logger.info(f"User with ser_id \'{user_id}\' sent new url: \'{url}\'")
    if url.startswith("https:") or url.startswith("http:"):
        summary = get_summary_from_url(url=url)
        logger.info(f"AI agent summarized content: \n\'{summary}\'")
        await message.answer(summary)
    else:
        logger.info(f"It was the bad url: \'{url}\'")
        await message.answer("Unfortunately, it was the bad url! Please, try again.")


# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    logger.info(f"Telegram bot started...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
