from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import *

def subs_start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(schedule_subs, 'cron', hour=0)
    scheduler.start()