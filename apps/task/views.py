import time


from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.blocking import BlockingScheduler
scheduler = BlockingScheduler()
# scheduler.add_jobstore(DjangoJobStore(), "default")


@register_job(scheduler, "interval", seconds=5, replace_existing=True)
def test_job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    print("I'm a test job!")
    # raise ValueError("Olala!")


# register_events(scheduler)

scheduler.start()
print("Scheduler started!")
