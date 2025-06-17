import asyncio
from aiogram import Bot, Dispatcher
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.handlers import router
from settings.config import TOKEN
from bot.utils import send_new_articles


bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main() -> None:
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        func=send_new_articles,
        trigger=CronTrigger.from_crontab("*/5 * * * *"),
        kwargs={'bot': bot}
    )
    scheduler.start()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.run_forever()
