import time
from django.db import connection
import datetime
from user.models import Ratings
from user.models import Movies
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from VideoRecommendSystem.wsgi import scheduler


@register_job(scheduler, "interval", seconds=5, id="test_job")
def test_job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"  I'm a test job!")

@register_job(scheduler, "interval", seconds=60, id="update_recommend_data")
def update_recommend_data():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "  update_recommend_data")
    ratings = Ratings.objects.filter(isupdate=1).only('user_id').distinct()
    if len(ratings)>0:
        for r in ratings:
            update_xsjz_and_recommendlist(r.user_id)
            Ratings.objects.filter(user_id=r.user_id).update(isupdate=0)
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"  更新用户"+str(r.user_id)+"推荐列表")


@register_job(scheduler, "interval", seconds=60, id="update_new_video")
def update_new_video(num=10):
    '''
    新电影被num个人观看之后，取消新电影的标记符号
    :return:
    '''
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+" update_new_video")
    movies = Movies.objects.filter(isnew=1)
    if len(movies)>0:
        for movie in movies:
            ratings = Ratings.objects.filter(movie_id=movie.movie_id)
            if len(ratings)>num:
                Movies.objects.filter(movie_id=movie.movie_id).update(isnew=0)
                print("视频"+str(movie.movie_id)+"取消新视频的标记")
#######################################################################################################################
def update_xsjz_and_recommendlist(userID):
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"   更新推荐数据开始")
    with connection.cursor() as cursor:
        cursor.callproc('update_xsjz_and_recommendlist', (userID,))  # 注意参数应该是一个元组
        connection.connection.commit()  # 调用存储过程后，确定要进行commit执行
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"   更新推荐数据结束")


