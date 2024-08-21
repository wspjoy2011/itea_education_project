from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def hello(request: HttpRequest, user_id: int):
    context = {'user_id': user_id}
    return render(request, 'blog/hello.html', context)
