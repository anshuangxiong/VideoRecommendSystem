from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from user.models import Sysusers
from recommend.models import Xsjz
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import Ratings
import logging
import json
from collections import defaultdict
import math
import operator
import time
import datetime
import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VideoRecommendSystem.settings")# project_name 项目名称
django.setup()



def recommend_userCF3():
    print("推荐开始   " + str(datetime.datetime.now()))
    users = Sysusers.objects.filter(user_id=1)#all().order_by('user_id')
    for user in users:
        # 获取用户观看过的视频
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
            print(str(user.user_id)+"  "+str(i)+"  :  "+str(rank[i]))

    print("推荐结束  " + str(datetime.datetime.now()))



recommend_userCF3()