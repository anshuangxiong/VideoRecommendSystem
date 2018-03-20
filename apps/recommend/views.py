from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from user.models import Movies
from user.models import Sysusers
from log.models import Movie80
from recommend.models import Xsjz
from recommend.models import Recommend
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import Ratings
import logging
import json
from collections import defaultdict
from django.db import connection
import math
import operator
import time
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
        print("推荐开始   " + str(datetime.datetime.now()))
        movies = Movies.objects.raw(
            'select m.movie_id,m.title,m.genres,m.year,m.m_desc from Movies m, recommend r where m.movie_id=r.movie_id and r.user_id='+userId+' order by r.recommend_score desc')[(page-1)*K:page*K]
        print("推荐结束   " + str(datetime.datetime.now()))
        movies = serializers.serialize("json", movies)
        json_data = json.dumps({'code': '0000', 'info': '成功', 'data': movies})
        # update_recommend_list2(104)
        # grapdata()
        return JsonResponse(json_data, safe=False, content_type='application/json')
    except KeyError as e:
        logger.error("当前没有用户登录")
        movies = Movies.objects.raw('select m.movie_id,m.title,m.genres,m.year,m.genres_en from MOVIES m,(select distinct r.movie_id from RATINGS r where r.rating=5) t where t.movie_id=m.movie_id')
        lists = []
        for movie in movies:
            lists.append(movie)
        paginator = Paginator(lists, 10)  # Show 10 contacts per page
        page = request.POST.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        lists = serializers.serialize("json", contacts)
        json_data = json.dumps({'code': '0000', 'info': '成功', 'data': lists})
        return JsonResponse(json_data,  safe=False, content_type='application/json')
########################################################################################


def update_recommend_list(userID):
    print(userID)
    print("更新推荐数据开始   " + str(datetime.datetime.now()))
    with connection.cursor() as cursor:
        # update_xsjz_and_recommendlist
        cursor.callproc('update_recommend_list', (userID,))  # 注意参数应该是一个元组
        connection.connection.commit()  # 调用存储过程后，确定要进行commit执行
    print("更新推荐数据结束   " + str(datetime.datetime.now()))

import requests
from bs4 import BeautifulSoup
import urllib
def graplink():
    # for movie in Movie80.objects.filter(mlink__isnull=True,mid>1082).order_by('mid'):
    for i in range(1):
        html = requests.get("http://www.80s.tw/movie/"+str(i+1114),verify=False)
        print(str(i+1114))
        soup = BeautifulSoup(html.text,'lxml')
        for mv in soup.select('#downid_0') :
            Movie80.objects.filter(mid=str(i+1114)).update(mlink=mv.attrs['value'])


def grapdata():
    start=1115
    for i in range(5):
        html = requests.get("http://www.80s.tw/movie/"+str((i+start)),verify=False)
        print(str((i+start)))
        soup = BeautifulSoup(html.text,'lxml')
        for mv in soup.select('.img') :
            src="http:"+mv.find_all('img')[0].attrs['src']
            urllib.request.urlretrieve(src, "static/image/"+str(i+start)+mv.find_all('img')[0].attrs['title']+'.jpg')
        mname=""
        mname2=""
        mactor=""
        mintroduce=""
        mscore=""
        mupdatedate=""
        mlength=""
        mstartdate=""
        mdirector=""
        mlanguage=""
        marea=""
        mtype=""
        mlink = ""
        for mv in soup.select('#downid_0'):
            mlink = mv.attrs['value']
        for mv in soup.find_all('div',{'class','info'}):
            mname=mv.find_all('h1')[0].get_text()
            for sp in mv.find_all('span',{'class','font_888'}):
                if sp.get_text()=="又名：":
                    mname2=str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("又名：","")
                if sp.get_text() == "演员：":
                    actor=""
                    for children in sp.parent.find_all('a'):
                        actor = actor+"|"+str(children.get_text());
                    mactor=actor
                if sp.get_text() == "类型：":
                    type=""
                    for children in sp.parent.find_all('a'):
                        type = type+" "+str(children.get_text());
                    mtype = type
                if sp.get_text() == "地区：":
                    area=""
                    for children in sp.parent.find_all('a'):
                        area = area+" "+str(children.get_text());
                    marea = area
                if sp.get_text() == "语言：":
                    language=""
                    for children in sp.parent.find_all('a'):
                        language = language+" "+str(children.get_text());
                    mlanguage = language
                if sp.get_text() == "导演：":
                    dao=""
                    for children in sp.parent.find_all('a'):
                        dao = dao+" "+str(children.get_text());
                    mdirector = dao
                if sp.get_text()=="上映日期：":
                    mstartdate = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("上映日期：","")
                if sp.get_text()=="片长：":
                    mlength = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("片长：","")
                if sp.get_text()=="更新日期：":
                    mupdatedate = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("更新日期：","")
                if sp.get_text()=="豆瓣评分：":
                    mscore = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("豆瓣评分：","")
                if sp.get_text()=="剧情介绍：":
                    mintroduce = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("剧情介绍：","")
        Movie80.objects.create(mid=str((i+start)),mname=mname,mname2=mname2,mactor=mactor,mtype=mtype,marea=marea,
                               mlanguage=mlanguage,mdirector=mdirector,mstartdate=mstartdate,mlength=mlength,
                               mupdatedate=mupdatedate,mscore=mscore,mintroduce=mintroduce,mlink=mlink)