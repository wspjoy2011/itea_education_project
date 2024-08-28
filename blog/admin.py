from django.contrib import admin
from django.utils.html import format_html

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'author', 'formatted_publish', 'thumbnail')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'body')
    list_filter = ('status', 'publish')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-status', '-publish')
    list_per_page = 20
    raw_id_fields = ('author',)

    readonly_fields = ('total_comments', 'total_likes', 'thumbnail', )

    def formatted_publish(self, obj):
        return obj.publish.strftime('%d %b %Y %H:%M:%S')

    formatted_publish.short_description = 'publish'
    formatted_publish.admin_order_field = 'publish'

    def thumbnail(self, obj):
        return format_html(f'<img src={obj.image_url} width="100" height="auto"')

    thumbnail.short_description = 'image'

    def total_comments(self, obj):
        return obj.comments.count()

    total_comments.short_description = 'total comments'

    def total_likes(self, obj):
        return obj.likes_count()

    total_likes.short_description = 'total likes'


@admin.register(models.PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    search_fields = ('user__username',)


@admin.register(models.PostDisLike)
class PostDisLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user')
    search_fields = ('user__username',)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created', 'author', 'active')
    list_filter = ('active', 'created')
    search_fields = ('author__username', 'body')
    actions = ('deactivate_comments', 'activate_comments')

    def deactivate_comments(self, request, queryset):
        queryset.update(active=False)

    def activate_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(models.CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user')
    search_fields = ('user__username',)


@admin.register(models.CommentDislike)
class CommentDislikeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user')
    search_fields = ('user__username',)
