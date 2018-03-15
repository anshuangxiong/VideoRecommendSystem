from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from user.models import Sysusers
from user.models import Movies
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import json
import logging


# Create your views here.


def administrator(request):
    '''
    后台管理首页
    :param request:
    :return:
    '''
    return render(request, 'admin.html')


@csrf_exempt
def videoList(request):
    movies = Movies.objects.all().order_by('movie_id').reverse()
    lists = []
    for movie in movies:
        movie_json = {"id": movie.movie_id, 'movie_title': movie.title,'year':movie.year, 'genres': movie.genres}
        lists.append(movie_json)
    return JsonResponse(lists,  safe=False, content_type='application/json')


@csrf_exempt
def userList(request):
    sysusers = Sysusers.objects.all().order_by('user_id')
    lists = []
    for user in sysusers:
        user_json = {"id": user.user_id, 'username': user.user_name, 'email': user.email,'state':user.state}
        lists.append(user_json)
    return JsonResponse(lists, safe=False, content_type='application/json')


@csrf_exempt
def removeVideo(request):
    movieId = request.POST.get('id')
    movieId=0
    try:
        row = Movies.objects.get(movie_id=movieId).delete()
        json_data = json.dumps({'code': '0000', 'info': '删除成功', 'data': row})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    except Exception:
        json_data = json.dumps({'code': '0001', 'info': '删除失败', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')


@csrf_exempt
def updateVideo(request):
    movieId = request.POST.get('id')
    movieName = request.POST.get('name')
    movieYear = request.POST.get('year')
    movieGenres = request.POST.get('genres')
    if movieId == '' or movieName == '' or movieYear == '' or movieGenres=='':
        json_data = json.dumps({'code': '0001', 'info': '参数不能为空', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    if len(Movies.objects.filter(movie_id=int(movieId))) >0:
        movie = Movies.objects.filter(movie_id=int(movieId)).update(title=movieName,year=movieYear,genres=movieGenres)
        json_data = json.dumps({'code': '0000', 'info': '更新成功', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    else:
        json_data = json.dumps({'code': '0002', 'info': '更新失败', 'data': ''})
        return JsonResponse(json_data,  safe=False, content_type='application/json')


@csrf_exempt
def userState(request):
    userId = request.POST.get('id')
    state = request.POST.get('state')
    if userId == '' or state == '' :
        json_data = json.dumps({'code': '0001', 'info': '参数不能为空', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    if len(Sysusers.objects.filter(user_id=int(userId))) >0:
        user = Sysusers.objects.filter(user_id=int(userId)).update(state=state)
        json_data = json.dumps({'code': '0000', 'info': '更新成功', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    else:
        json_data = json.dumps({'code': '0002', 'info': '更新失败', 'data': ''})
        return JsonResponse(json_data,  safe=False, content_type='application/json')



@csrf_exempt
def addVideo(request):
    name = request.POST.get('name')
    year = request.POST.get('year')
    genres = request.POST.get('genres')
    if name == '' or year == '' or genres == '':
        json_data = json.dumps({'code': '0001', 'info': '参数不能为空', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    else:
        max_id=Movies.objects.all().order_by('movie_id').reverse()[0].movie_id
        Movies.objects.create(movie_id=int(max_id)+1,title=str(name),year=str(year),genres=genres)
        json_data = json.dumps({'code': '0000', 'info': '添加成功', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')




