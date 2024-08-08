from datetime import datetime
from .job import api_schedule,print_result
from apscheduler.schedulers.background import BackgroundScheduler
def strat():
    scheduler = BackgroundScheduler()
    scheduler.add_job(print_result, 'interval', seconds=10)
    scheduler.start()