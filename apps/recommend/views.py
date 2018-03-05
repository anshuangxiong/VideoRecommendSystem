from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from user.models import Movies
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from user.models import Ratings
import json
# Create your views here.


@csrf_exempt
def recommend_best_score(request):
    try:
        user = request.session["user"]
        print(user['fields']['user_name'])
        json_data = json.dumps({'code': '0000', 'info': '成功', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    except KeyError:
        print("当前没有用户登录")
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

