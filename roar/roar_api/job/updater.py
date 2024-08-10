from datetime import datetime
from .job import print_result
from apscheduler.schedulers.background import BackgroundScheduler
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(print_result, 'cron', hour=0, minute=0, id='cron_task')
    scheduler.start()