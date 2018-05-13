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
from django.conf.urls import url
from administrator import views
app_name='[administrator]'
urlpatterns = [
    url(r'^videoList', views.videoList, name='videoList'),
    url(r'^userList', views.userList, name='userList'),
    url(r'^removeVideo', views.removeVideo, name='removeVideo'),
    url(r'^updateVideo', views.updateVideo, name='updateVideo'),
    url(r'^userState', views.userState, name='userState'),
    url(r'^addVideo', views.addVideo, name='addVideo'),
    url(r'^getRecommendData', views.getRecommendData, name='getRecommendData'),
    url(r'^getSimiliarData', views.getSimiliarData, name='getSimiliarData'),


]
