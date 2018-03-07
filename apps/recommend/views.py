from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from user.models import Movies
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import Ratings
import logging
import json
from collections import defaultdict
import math
import operator
import time
# Create your views here.
logger = logging.getLogger(__name__)

@csrf_exempt
def recommend_best_score(request):
    try:
        user = request.session["user"]
        print("用户登录："+user['fields']['user_name']+"  userID:  "+str(user['pk']))
        user2item_matrix, item2user_matrix = get_data()
        W = user_sim_cosine(user2item_matrix)
        rank_list = recommend_userCF(user2item_matrix, str(user['pk']), W, int(9999))
        movie_ids=[]
        for i in range(len(rank_list)):
            movie_ids.append(int(rank_list[i][0]))
        movies = Movies.objects.filter(movie_id__in=movie_ids)
        paginator = Paginator(movies, 10)  # Show 10 contacts per page
        page = request.POST.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)
        movies = serializers.serialize("json", contacts)
        json_data = json.dumps({'code': '0000', 'info': '成功', 'data': movies})
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
    for i in user_list:
        for j in user_list:
            if i == j:
                continue
            W[i][j] = len(set(user2item_matrix[i].keys()) & set(user2item_matrix[j].keys()))  # 交集
            W[i][j] /= math.sqrt(len(user2item_matrix[i].keys()) * len(user2item_matrix[j].keys()) * 1.0)
    return W


def item_sim_cosine(item2user_matrix):
    W = defaultdict(defaultdict)  # 物品-物品-相似度矩阵
    item_list = item2user_matrix.keys()
    for i in item_list:
        for j in item_list:
            if i == j:
                continue
            W[i][j] = len(set(item2user_matrix[i].keys()) & set(item2user_matrix[j].keys())) # 交集
            W[i][j] /= math.sqrt(len(item2user_matrix[i].keys())*len(item2user_matrix[j].keys())*1.0)
    return W


def recommend_userCF(user2item_matrix, user_id, W, K=10):
    '''通过用户userid、训练集数据、用户相似度矩阵进行topN推荐'''
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
