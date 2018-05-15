from __future__ import absolute_import
from celery import shared_task
from celery import task
import time

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@task
def my_job():
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))