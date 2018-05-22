from django.contrib import admin
# Register your models here.

from user.models import *
admin.site.register(Movies)
admin.site.register(Ratings)
admin.site.register(Links)
admin.site.register(Sysusers)

