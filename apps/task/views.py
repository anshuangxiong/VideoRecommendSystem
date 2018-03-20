import time
from django.db import connection
import datetime
from user.models import Ratings
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

def update_recommend_data():
    for r in Ratings.objects.filter(isupdate=1).only('user_id').distinct():
        update_xsjz_and_recommendlist(r.user_id)


def update_xsjz_and_recommendlist(userID):
    print("更新推荐数据开始   " + str(datetime.datetime.now()))
    with connection.cursor() as cursor:
        cursor.callproc('update_xsjz_and_recommendlist', (userID,))  # 注意参数应该是一个元组
        connection.connection.commit()  # 调用存储过程后，确定要进行commit执行
    print("更新推荐数据结束   " + str(datetime.datetime.now()))

