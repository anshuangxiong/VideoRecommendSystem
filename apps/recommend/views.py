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
        # recommend_userCF3()
        # grapdata()
        # update_recommend_list2(104)
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


def get_data():
    user2item_matrix = defaultdict(defaultdict)  # 用户到物品的评分矩阵
    item2user_matrix = defaultdict(defaultdict)  # 物品到用户的倒排评分矩阵
    print("读取数据开始"+str(time.time()))
    logger.info("读取数据开始"+str(time.time()))
    ratings = Ratings.objects.all()
    for rating in ratings:
        userID, movieID, score = rating.user_id, rating.movie_id, rating.rating
        user2item_matrix[str(userID)][str(movieID)] = float(score)
        item2user_matrix[str(movieID)][str(userID)] = float(score)
    logger.info("读取数据结束" + str(time.time()))
    print("读取数据结束" + str(time.time()))
    return user2item_matrix, item2user_matrix


def user_sim_cosine(user2item_matrix):
    W = defaultdict(defaultdict)  # 用户-用户-相似度矩阵
    user_list = user2item_matrix.keys()
    print("开始计算相似矩阵")
    for i in user_list:
        for j in user_list:
            if i == j:
                continue
            W[i][j] = len(set(user2item_matrix[i].keys()) & set(user2item_matrix[j].keys()))  # 交集
            W[i][j] /= math.sqrt(len(user2item_matrix[i].keys()) * len(user2item_matrix[j].keys()) * 1.0)
    print("相似矩阵计算结束")
    return W


def item_sim_cosine(item2user_matrix):
    W = defaultdict(defaultdict)  # 物品-物品-相似度矩阵
    item_list = item2user_matrix.keys()
    print("开始计算相似矩阵")
    for i in item_list:
        for j in item_list:
            if i == j:
                continue
            W[i][j] = len(set(item2user_matrix[i].keys()) & set(item2user_matrix[j].keys())) # 交集
            W[i][j] /= math.sqrt(len(item2user_matrix[i].keys())*len(item2user_matrix[j].keys())*1.0)
    print("相似矩阵计算结束")
    return W


def recommend_userCF(user2item_matrix, user_id, W, K=10):
    '''通过用户userid、训练集数据、用户相似度矩阵进行topN推荐'''
    print("开始推荐")
    rank=defaultdict(int)
    # 获取用户的物品列表

    user_item_set = user2item_matrix[user_id].keys()
    # 遍历与该user_id相似的用户和相似度得分
    for w_userid,w_score in sorted(W[user_id].items(),key=operator.itemgetter(1),reverse=True)[0:K]:
        # 遍历相似用户看过的物品与打分
        for item_id,item_score in user2item_matrix[w_userid].items():
            # 如果相似用户看过的电影也在目标用户的物品集合中，则忽略该物品的推荐
            if item_id in user_item_set:
                continue
            # 计算该物品推荐给用户的排序分  用户的相似度*评分
            rank[item_id] = w_score*item_score

    # 对所有推荐物品与打分按照排序分进行降序排序，取前K个物品
    rank_list = sorted(rank.items(),key=operator.itemgetter(1),reverse=True)[0:K]
    print("推荐结束")
    return rank_list


def recommend_userCF2(user_id, page, K=10):
    user_id = 2
    page = int(page)
    print("推荐开始   " + str(datetime.datetime.now()))
    rank = defaultdict(int)
    # 获取用户观看过的视频
    user_items = Ratings.objects.filter(user_id=user_id)
    movie_ids=[] # 所有看过的视频id 组成的list
    for user_item in user_items:
        movie_ids.append(user_item.movie_id)
    # 该用户和其他用户之间的相似度  按相似度从大到小排序 取出第page页
    xsjzs = Xsjz.objects.filter(r=int(user_id)).exclude(v=0).order_by('v').reverse()#[(page-1)*10:page*K]
    print(len(xsjzs))
    commend = open("recommend.txt",'w')
    for xsjz in xsjzs:
        # 获取相似用户看过的视频  按评分从大到小排序
        items = Ratings.objects.filter(user_id=xsjz.c).order_by('rating').reverse()#[(page-1)*10:page*K]
        for item in items:
            # 判断相似用户看过的视频该用户已经看过 若看过 不推荐 没有看过  计算推荐度(用户之间的相似度*相似用户对该电影的评分)
            if item.movie_id in movie_ids:
                continue
            tmp = xsjz.v * item.rating
            if tmp > rank[item.movie_id]:
                rank[item.movie_id] = tmp
    print(len(rank))
    # 对推荐度进行从大到小排序 取出前K个返回
    rank_list = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)[(page-1)*10:page*K]#[0:K]
    print("推荐结束  " + str(datetime.datetime.now()))
    return rank_list


def recommend_ItemCF(user2item_matrix, user_id, W, K=10):
    '''通过用户userid、训练集数据、用户相似度矩阵进行topN推荐'''
    rank=defaultdict(int)
    # 获取用户的物品列表
    user_item_set = user2item_matrix[user_id].keys()

    # 遍历用户喜欢的物品列表
    for item, item_score in user2item_matrix[user_id].items():
        # 遍历与该物品相似的物品
        for w_itemid, w_score in sorted(W[item].items(), key=operator.itemgetter(1), reverse=True)[0:K]:
            # 如果相似用户看过的电影也在目标用户的物品集合中，则忽略该物品的推荐
            if w_itemid in user_item_set:
                continue
            # 计算该物品推荐给用户的排序分
            rank[w_itemid] = w_score * item_score
    # 对所有推荐物品与打分按照排序分进行降序排序，取前K个物品
    rank_list = sorted(rank.items(),key=operator.itemgetter(1),reverse=True)[0:K]
    return rank_list




def recommend_userCF3():
    print("推荐开始   " + str(datetime.datetime.now()))
    # for i in range(671):
    #     print(i)
    #     Sysusers.objects.create(user_id=i+1,user_name='test'+str(i+1),password='123456',email='13821752883@163.com',state=1)
    users = Sysusers.objects.all().order_by('user_id')
    for user in users:
        #获取用户观看过的视频
        user_items = Ratings.objects.filter(user_id=user.user_id)
        movie_ids=[] # 所有看过的视频id 组成的list
        for user_item in user_items:
            movie_ids.append(user_item.movie_id)
        # 该用户和其他用户之间的相似度  按相似度从大到小排序
        xsjzs = Xsjz.objects.filter(r=int(user.user_id)).exclude(v=0).order_by('v').reverse()
        rank = defaultdict(int)
        for xsjz in xsjzs:
            # 获取相似用户看过的视频  按评分从大到小排序
            items = Ratings.objects.filter(user_id=xsjz.c).order_by('rating').reverse()
            for item in items:
                # 判断相似用户看过的视频该用户已经看过 若看过 不推荐 没有看过  计算推荐度(用户之间的相似度*相似用户对该电影的评分)
                if item.movie_id in movie_ids:
                    continue
                tmp = xsjz.v * item.rating
                if tmp > rank[item.movie_id]:
                    rank[item.movie_id] = tmp
        for i in rank.keys():
            # print(str(user.user_id)+"  "+str(i)+"  :  "+str(rank[i]))
            Recommend.objects.create(user_id=user.user_id,movie_id=i,recommend_score=rank[i])
    print("推荐结束  " + str(datetime.datetime.now()))


import requests
from bs4 import BeautifulSoup
import urllib
def grapdata():
    start=1028
    for i in range(1000):
        html = requests.get("http://www.80s.tw/movie/"+str((i+start)),verify=False)
        print(str((i+start)))
        soup = BeautifulSoup(html.text,'lxml')
        for mv in soup.select('.img') :#find_all('div',{'class','img'}):
            src="http:"+mv.find_all('img')[0].attrs['src']
            urllib.request.urlretrieve(src, "data/"+str(i+start)+mv.find_all('img')[0].attrs['title']+'.jpg')

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
        for mv in soup.find_all('div',{'class','info'}):
            mname=mv.find_all('h1')[0].get_text()
            #print(mname)
            for sp in mv.find_all('span',{'class','font_888'}):
                if sp.get_text()=="又名：":
                    mname2=str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("又名：","")
                    #print(mname2)
                if sp.get_text() == "演员：":
                    actor=""
                    for children in sp.parent.find_all('a'):
                        actor = actor+"|"+str(children.get_text());
                    mactor=actor
                    #print(mactor)
                if sp.get_text() == "类型：":
                    type=""
                    for children in sp.parent.find_all('a'):
                        type = type+" "+str(children.get_text());
                    mtype = type
                    #print(mtype)
                if sp.get_text() == "地区：":
                    area=""
                    for children in sp.parent.find_all('a'):
                        area = area+" "+str(children.get_text());
                    marea = area
                    #print(marea)
                if sp.get_text() == "语言：":
                    language=""
                    for children in sp.parent.find_all('a'):
                        language = language+" "+str(children.get_text());
                    mlanguage = language
                    #print(mlanguage)
                if sp.get_text() == "导演：":
                    dao=""
                    for children in sp.parent.find_all('a'):
                        dao = dao+" "+str(children.get_text());
                    mdirector = dao
                    #print(mdirector)
                if sp.get_text()=="上映日期：":
                    mstartdate = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("上映日期：","")
                    #print(mstartdate)
                if sp.get_text()=="片长：":
                    mlength = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("片长：","")
                    #print(mlength)
                if sp.get_text()=="更新日期：":
                    mupdatedate = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("更新日期：","")
                    #print(mupdatedate)
                if sp.get_text()=="豆瓣评分：":
                    mscore = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("豆瓣评分：","")
                    #print(mscore)
                if sp.get_text()=="剧情介绍：":
                    mintroduce = str(sp.parent.get_text()).replace("\n","").replace(" ","").replace("剧情介绍：","")
                    #print(mintroduce)
        Movie80.objects.create(mid=str((i+start)),mname=mname,mname2=mname2,mactor=mactor,mtype=mtype,marea=marea,
                               mlanguage=mlanguage,mdirector=mdirector,mstartdate=mstartdate,mlength=mlength,
                               mupdatedate=mupdatedate,mscore=mscore,mintroduce=mintroduce)


def update_recommend_list(userID):
    print(userID)
    # 删除该用户的推荐列表
    Recommend.objects.filter(user_id=userID).delete()
    print("更新开始   " + str(datetime.datetime.now()))
    #获取用户观看过的视频
    user_items = Ratings.objects.filter(user_id=userID)
    movie_ids=[] # 所有看过的视频id 组成的list
    for user_item in user_items:
        movie_ids.append(user_item.movie_id)
    # 该用户和其他用户之间的相似度  按相似度从大到小排序
    xsjzs = Xsjz.objects.filter(r=int(userID)).exclude(v=0).order_by('v').reverse()
    rank = defaultdict(int)
    for xsjz in xsjzs:
        # 获取相似用户看过的视频  按评分从大到小排序
        items = Ratings.objects.filter(user_id=xsjz.c).order_by('rating').reverse()
        for item in items:
            # 判断相似用户看过的视频该用户已经看过 若看过 不推荐 没有看过  计算推荐度(用户之间的相似度*相似用户对该电影的评分)
            if item.movie_id in movie_ids:
                continue
            tmp = xsjz.v * item.rating
            if tmp > rank[item.movie_id]:
                rank[item.movie_id] = tmp
    for i in rank.keys():
        Recommend.objects.create(user_id=userID,movie_id=i,recommend_score=rank[i])
    print("更新结束  " + str(datetime.datetime.now()))


def update_recommend_list2(userID):
    print(userID)
    print("更新推荐数据开始   " + str(datetime.datetime.now()))
    with connection.cursor() as cursor:
        cursor.callproc('update_recommend_list', (userID,))  # 注意参数应该是一个元组
        connection.connection.commit()  # 调用存储过程后，确定要进行commit执行
    print("更新推荐数据结束   " + str(datetime.datetime.now()))