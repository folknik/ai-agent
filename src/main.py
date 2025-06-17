import asyncio
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.bot import bot, dp, collect_habr_content


async def main() -> None:
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        func=collect_habr_content,
        trigger=CronTrigger.from_crontab("*/5 * * * *")
    )
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.run_forever()
