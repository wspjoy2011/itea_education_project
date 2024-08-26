from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from blog import models


def hello(request: HttpRequest, user_id: int):
    context = {'user_id': user_id}
    return render(request, 'blog/hello.html', context)


def posts(request: HttpRequest):
    posts = models.Post.objects.all()
    context = {'posts': posts}
    return render(request, 'blog/posts.html', context)

def comment(request: HttpRequest, post_id: int):
    comments = models.Comment.objects.filter(post_id=post_id)
    # context = {'comments':comment}
    return render(request, "blog/post.html", {"comments":comments})

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html",{"question": question}) 
