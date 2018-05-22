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
        rating = Ratings.objects.filter(user_id=int(userId), movie_id=int(movieId)).update(rating=score,timestamp = int(time.time()),isupdate=1)
        json_data = json.dumps({'code': '0000', 'info': '更新成功', 'data': ''})
        # update_xsjz_and_recommendlist(userId)
        return JsonResponse(json_data, safe=False, content_type='application/json')
    else:
        Ratings.objects.create(user_id=userId, movie_id=movieId, rating=score,timestamp=int(time.time()),isupdate=1)
        json_data = json.dumps({'code': '0000', 'info': '评论成功', 'data': ''})
        # update_xsjz_and_recommendlist(userId)
        return JsonResponse(json_data,  safe=False, content_type='application/json')

##########################################################################################


