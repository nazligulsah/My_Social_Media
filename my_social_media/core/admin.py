from django.contrib import admin
from .models import Account,Post,Liked, Follow
# Register your models here.

admin.site.register(Account)
admin.site.register(Post)
admin.site.register(Liked)
admin.site.register(Follow)