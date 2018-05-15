# coding:utf8
from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' program.

# 这里我使用生产的配置，这里有点瑕疵，不会指定上面导入的settings，导致开发环境和生产环境没办法区分，想到办法再更新
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VideoRecommendSystem.prod_settings')

app = Celery('VideoRecommendSystem')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))