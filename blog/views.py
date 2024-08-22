from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from blog import models


def hello(request: HttpRequest, user_id: int):
    context = {'user_id': user_id}
    return render(request, 'blog/hello.html', context)


def posts(request: HttpRequest):
    posts = models.Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/posts.html', context)
