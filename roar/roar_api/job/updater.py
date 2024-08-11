from datetime import datetime
from .job import print_result
from apscheduler.schedulers.background import BackgroundScheduler
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(print_result, 'cron', hour=22, minute=19, id='cron_task')
    scheduler.start()