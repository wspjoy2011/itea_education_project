from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views import View

from blog.models import Post


class PostPermissionMixin(View):
    def dispatch(self, request, *args, **kwargs):
        post_slug = kwargs.get('post_slug')
        post = self.get_post_by_slug(post_slug)

        if not request.user.is_superuser and not request.user == post.author:
            return HttpResponseForbidden("You don't have permission to delete this post")

        return super().dispatch(request, *args, **kwargs)

    def get_post_by_slug(self, post_slug):
        return get_object_or_404(Post, slug=post_slug)
