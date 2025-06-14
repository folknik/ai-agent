import os
import asyncio
from dotenv import load_dotenv
from langchain_openai import OpenAI
from aiogram.types import Message
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TOKEN = os.getenv("BOT_TOKEN")


user_prompt = """
Перейди по ссылке: {url}. Прочитай статью и суммируй её суть в 2 абзацах.
"""

llm = OpenAI(
    model="gpt-4o-mini",
    api_key=OPENAI_API_KEY,
    temperature=0.1,
    max_retries=0,
    max_tokens=2000
)


dp = Dispatcher()


def run_agent(url: str) -> str:
    inputs = [
        {
            "role": "system",
            "content": user_prompt.format(url=url)
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
    if text.startswith("https:") or text.startswith("http:"):
        summary = run_agent(url=text)
        await message.answer(summary)
    else:
        await message.answer("Unfortunately, no links were found.")


# Run the bot
async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
