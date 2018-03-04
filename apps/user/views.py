from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from user.models import Movies
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


def index(request):
    '''
    首页
    :param request:
    :return:
    '''
    return render(request, 'index.html')


@csrf_exempt
def type(request):
    movies = Movies.objects.filter(movie_id__lt=10).distinct()
    movies = serializers.serialize("json", movies)
    json_data = json.dumps({'code': '0000', 'info': '成功', 'data': movies})
    return JsonResponse(json_data,  safe=False, content_type='application/json')


@csrf_exempt
def movie_list_by_type(request):
    movie_type = request.POST['movie_type']
    movies = Movies.objects.filter(genres__contains=movie_type).distinct()
    paginator = Paginator(movies, 10)  # Show 10 contacts per page
    page = request.POST.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    print(len(contacts))
    movies = serializers.serialize("json", contacts)
    json_data = json.dumps({'code': '0000', 'info': '成功', 'data': movies})
    return JsonResponse(json_data,  safe=False, content_type='application/json')