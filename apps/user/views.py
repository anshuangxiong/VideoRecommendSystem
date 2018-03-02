from django.shortcuts import render
from user.models import Movies
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def type(request):
    movies = Movies.objects.filter(movie_id__lt=100).distinct()
    movies = serializers.serialize("json", movies)
    json_data = json.dumps({'code': '0000', 'info': '成功', 'data': movies})
    return JsonResponse(json_data,  safe=False, content_type='application/json')

