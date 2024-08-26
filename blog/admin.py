from django.contrib import admin

from . import models


@admin.register(models.PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    search_fields = ('user__username',)


@admin.register(models.PostDisLike)
class PostDisLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    search_fields = ('user__username',)
