"""VideoRecommendSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import user
import administrator


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^log/', include('log.urls', namespace='log')),  # 日志模块
    url(r'^user/', include('user.urls', namespace='user')),  # 用户模块
    url(r'^recommend/', include('recommend.urls', namespace='recommend')),  # 推荐模块
    url(r'^administrator/', include('administrator.urls', namespace='administrator')),  # 后台管理模块
    url(r'^$', user.views.index, name='index'),  # 首页
    url(r'^video/admin$', administrator.views.administrator, name='administrator'),  # 后台管理
]

# import task.views
