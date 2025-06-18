import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from settings.config import TOKEN
from settings.logger import get_logger
from bot.handlers import router
from bot.utils import send_new_articles


logger = get_logger(__name__)


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def main() -> None:
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        func=send_new_articles,
        trigger=CronTrigger.from_crontab("*/5 * * * *"),
        kwargs={'bot': bot}
    )
    scheduler.start()

    try:
        dp.include_router(router)
        await dp.start_polling(bot)
    except Exception as exc:
        logger.debug(f"Error occurred: {exc}")


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.run_forever()
