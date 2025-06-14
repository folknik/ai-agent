import logging
import asyncio
from langchain_openai import OpenAI
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart

from src.config import *


logger = logging.getLogger(__name__)


llm = OpenAI(
    model=LLM_MODEL,
    api_key=OPENAI_API_KEY,
    temperature=LLM_TEMPERATURE,
    max_tokens=LLM_MAX_TOKENS,
    max_retries=LLM_MAX_RETRIES
)


dp = Dispatcher()


def run_agent(url: str) -> str:
    inputs = [
        {
            "role": "system",
            "content": PROMPT.format(url=url)
        }
    ]
    response = llm.invoke(inputs)
    return response


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
    text = message.text
    logger.info(f"New text: \'{text}\'")
    if text.startswith("https:") or text.startswith("http:"):
        summary = run_agent(url=text)
        logger.info(f"AI agnet summarized content: \n\'{summary}\'")
        await message.answer(summary)
    else:
        logger.info(f"It was a bad text: \'{text}\'")
        await message.answer("Unfortunately, no link was found. Try again.")


# Run the bot
async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)
    logger.info(f"Telegram bot started...")


if __name__ == '__main__':
    asyncio.run(main())
