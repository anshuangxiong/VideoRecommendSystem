from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from user.models import Movies
from user.models import Sysusers
from django.core import serializers
import logging
import json
import datetime

# Create your views here.
logger = logging.getLogger(__name__)


@csrf_exempt
def recommend_best_score(request):
    try:
        user = request.session["user"]
        print("登录用户："+user['fields']['user_name']+"  userID:  "+str(user['pk']))
        page = request.POST.get('page')
        K=10
        page=int(page)
        userId = str(user['pk'])
        print("按推荐算法开始推荐   " + str(datetime.datetime.now()))
        movies = Movies.objects.raw(
            'select m.movie_id,m.title,m.genres,m.year,m.description,'
            'm.movie_name,m.show_year,m.director,m.leadactors,m.picture,'
            'm.averating,m.typelist,m.backpost,r.recommend_score '
            'from Movies m , recommend r '
            'where m.movie_id=r.movie_id and r.user_id='+userId+' order by r.recommend_score desc,m.movie_id')[(page-1)*K:page*K]
        print("按推荐算法推荐结束   " + str(datetime.datetime.now()))
        for movie in movies:
            movie.recommend_score=round(movie.recommend_score,2)
        if len(movies)==0:
            movies = recommend_by_user_hobby(user['pk'],page,K)
        movies = serializers.serialize("json", movies)
        json_data = json.dumps({'code': '0000', 'info': '成功', 'data': movies})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    except KeyError as e:
        logger.error("当前没有用户登录")
        page = request.POST.get('page')
        K = 10
        page = int(page)
        movies = Movies.objects.all().order_by('-isnew','-averating','movie_id')[(page-1)*K:page*K]
        movies = serializers.serialize("json", movies)
        json_data = json.dumps({'code': '0000', 'info': '成功', 'data': movies})
        return JsonResponse(json_data,  safe=False, content_type='application/json')



def recommend_by_user_hobby(userId,page,K):
    print("按用户爱好开始推荐   " + str(datetime.datetime.now()))
    user = Sysusers.objects.get(user_id=userId)
    hobbys = user.hobby.split(',')
    sql = ""
    param = []
    for hobby in hobbys:
        tmp = "%"+hobby+"%"
        param.append(tmp)
        if sql=="":
            sql =sql+  "select  t.movie_id,t.title,t.genres,t.genres_en,t.year,to_char(t.description),t.movie_name,t.show_year,t.director,t.leadactors,t.picture,t.averating,t.typelist,to_char(t.backpost) from MOVIES t where t.genres_en like %s";
        else:
            sql= sql+ " union "+ "select  t.movie_id,t.title,t.genres,t.genres_en,t.year,to_char(t.description),t.movie_name,t.show_year,t.director,t.leadactors,t.picture,t.averating,t.typelist,to_char(t.backpost) from MOVIES t where t.genres_en like %s";
    print(sql)
    movies = Movies.objects.raw(sql,param)[(page-1)*K:page*K]
    print("按用户爱好推荐结束   " + str(datetime.datetime.now()))
    return movies
########################################################################################




