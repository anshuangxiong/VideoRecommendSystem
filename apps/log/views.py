from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from recommend.models import Recommend
from recommend.models import Xsjz
from user.models import Ratings
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from collections import defaultdict
import json
import time
import datetime
import logging

# Create your views here.


@csrf_exempt
def insert_score(request):
    userId = request.POST.get('userId')
    movieId = request.POST.get('movieId')
    score = request.POST.get('score')
    if userId == '' or movieId == '' or score == '':
        json_data = json.dumps({'code': '0001', 'info': '参数不能为空', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    if len(Ratings.objects.filter(user_id=int(userId), movie_id=int(movieId)))>0:
        rating = Ratings.objects.filter(user_id=int(userId), movie_id=int(movieId)).update(rating=score,timestamp = int(time.time()))
        json_data = json.dumps({'code': '0000', 'info': '更新成功', 'data': ''})
        update_xsjz_and_recommendlist(userId)
        return JsonResponse(json_data, safe=False, content_type='application/json')
    else:
        Ratings.objects.create(user_id=userId, movie_id=movieId, rating=score,timestamp=int(time.time()))
        json_data = json.dumps({'code': '0000', 'info': '评论成功', 'data': ''})
        update_xsjz_and_recommendlist(userId)
        return JsonResponse(json_data,  safe=False, content_type='application/json')

##########################################################################################


def update_xsjz(userID):
    print("更新相似矩阵开始   " + str(datetime.datetime.now()))
    with connection.cursor() as cursor:
        cursor.callproc('update_xsjz', (userID,))  # 注意参数应该是一个元组
        connection.connection.commit()  # 调用存储过程后，确定要进行commit执行
    print("更新相似矩阵结束   " + str(datetime.datetime.now()))


def update_recommend_list(userID):
    # 删除该用户的推荐列表
    Recommend.objects.filter(user_id=userID).delete()
    print("更新推荐列表开始   " + str(datetime.datetime.now()))
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
    print("更新推荐列表结束  " + str(datetime.datetime.now()))


def update_recommend_list2(userID):
    print(userID)
    print("更新推荐列表开始   " + str(datetime.datetime.now()))
    with connection.cursor() as cursor:
        cursor.callproc('update_recommend_list', (userID,))  # 注意参数应该是一个元组
        connection.connection.commit()  # 调用存储过程后，确定要进行commit执行
    print("更新推荐列表结束   " + str(datetime.datetime.now()))


def update_xsjz_and_recommendlist(userID):
    print("更新推荐数据开始   " + str(datetime.datetime.now()))
    with connection.cursor() as cursor:
        cursor.callproc('update_xsjz_and_recommendlist', (userID,))  # 注意参数应该是一个元组
        connection.connection.commit()  # 调用存储过程后，确定要进行commit执行
    print("更新推荐数据结束   " + str(datetime.datetime.now()))