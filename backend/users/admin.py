from django.contrib.admin import ModelAdmin, register
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Follow


@register(CustomUser)
class MyUserAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name',
                    'password')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


@register(Follow)
class FollowAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
