import time
from apscheduler.schedulers.blocking import BlockingScheduler


def my_job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"1234")



#sched = BlockingScheduler()
#sched.add_job(my_job, 'interval', seconds=5)
#sched.start()


from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

jobstores = {
    'mongo': MongoDBJobStore(),
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

scheduler.add_job(my_job, 'interval', seconds=5)
scheduler.start()
