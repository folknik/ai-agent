from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.blocking import BlockingScheduler

SCHEDULER = BlockingScheduler(timezone="UTC")
TRIGGER = CronTrigger.from_crontab("30 6 * * *")
