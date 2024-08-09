from datetime import datetime
from .job import print_result
from apscheduler.schedulers.background import BackgroundScheduler
def strat():
    scheduler = BackgroundScheduler()
    scheduler.add_job(print_result, 'interval', seconds=100)
    scheduler.start()