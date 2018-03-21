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
logger = logging.getLogger(__name__)

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
    logger.info('movie_type:'+movie_type)
    find_text = request.POST.get('findtext')
    if find_text != '':
        movies = Movies.objects.filter(title__contains=find_text).distinct().order_by('movie_id')
    else:
        movies = Movies.objects.filter(genres__contains=movie_type).distinct().order_by('-isnew','movie_id')
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
    return JsonResponse(json_data,  safe=False, content_type='application/json')


@csrf_exempt
def user_login(request):
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')

    users=Sysusers.objects.filter(user_name=username,password=pwd,state=1)
    # 先序列化
    users = serializers.serialize('json', users)
    # 转换为字典类型
    users = json.loads(users)
    if len(users)>0:
        # 登录成功放入session
        request.session["user"] = users[0]
        request.session["username"] = users[0]['fields']['user_name']
        login_data = {'username': users[0]['fields']['user_name']}
        json_data = json.dumps({'code': '0000', 'info': '登录成功', 'data': login_data})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    else:
        json_data = json.dumps({'code': '0001', 'info': '登录失败', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')


@csrf_exempt
def user_logout(request):
    del(request.session["user"])
    del(request.session["username"])
    json_data = json.dumps({'code': '0000', 'info': '退出成功', 'data': ''})
    return JsonResponse(json_data, safe=False, content_type='application/json')


@csrf_exempt
def user_register(request):
    username = request.POST.get('username')
    pwd = request.POST.get('pwd')
    email = request.POST.get('email')
    hobby = request.POST.get('hobby')
    if username == '' or pwd == '' or email == '' or hobby == '':
        json_data = json.dumps({'code': '0002', 'info': '参数不能为空', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    users = Sysusers.objects.filter(user_name=username)
    if len(users) > 0:
        json_data = json.dumps({'code': '0001', 'info': '对不起用户名已存在', 'data': ''})
        return JsonResponse(json_data, safe=False, content_type='application/json')
    with connection.cursor() as cursor:
        cursor.execute("select VIDEO_USER_SEQ.nextval from dual")
        row = cursor.fetchone()
    Sysusers.objects.create(user_id=int(row[0]),user_name=str(username),password=str(pwd),email=email,hobby=hobby,state=1)
    register_data = {'username': username}
    json_data = json.dumps({'code': '0000', 'info': '注册成功', 'data': register_data})
    return JsonResponse(json_data, safe=False, content_type='application/json')



