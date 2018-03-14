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
    movies = Movies.objects.all()
    lists = []
    for movie in movies:
        movie_json = {"id": movie.movie_id, 'movie_title': movie.title, 'genres': movie.genres}
        lists.append(movie_json)
    return JsonResponse(lists,  safe=False, content_type='application/json')


@csrf_exempt
def userList(request):
    sysusers = Sysusers.objects.all()
    lists = []
    for user in sysusers:
        user_json = {"id": user.user_id, 'username': user.user_name, 'email': user.email}
        lists.append(user_json)
    return JsonResponse(lists, safe=False, content_type='application/json')