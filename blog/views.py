from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from urllib.parse import urlencode

from django.views.generic import ListView

from .models import Post


def post_list(request):
    queryset = Post.published.all()
    page = request.GET.get('page')
    per_page = 4
    period = request.GET.get('period')

    if period == 'day':
        today = timezone.localtime().date()
        queryset = queryset.filter(publish__date=today)
    elif period == 'week':
        start_date = timezone.localtime().date() - timezone.timedelta(days=7)
        queryset = queryset.filter(publish__gte=start_date)
    elif period == 'month':
        start_date = timezone.localtime().date() - timezone.timedelta(days=30)
        queryset = queryset.filter(publish__gte=start_date)
    elif period == 'year':
        current_year = timezone.localtime().year
        queryset = queryset.filter(publish__year=current_year)

    paginator = Paginator(queryset, per_page)

    try:
        queryset_paginated = paginator.page(page)
    except PageNotAnInteger:
        queryset_paginated = paginator.page(1)
    except EmptyPage:
        queryset_paginated = paginator.page(paginator.num_pages)

    query_params = request.GET.copy()
    query_params.pop('page', None)
    query_string = urlencode(query_params)

    if query_string:
        query_string = '&' + query_string

    context = {
        'posts': queryset_paginated,
        'query_string': query_string
    }
    return render(request, 'blog/post/list.html', context)


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(
        Post,
        slug=post_slug,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status='p'
    )
    context = {
        'post': post
    }
    return render(request, 'blog/post/detail.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/post/list.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        queryset = Post.published.all()
        period = self.request.GET.get('period')

        if period == 'day':
            today = timezone.localtime().date()
            queryset = queryset.filter(publish__date=today)
        elif period == 'week':
            start_date = timezone.localtime().date() - timezone.timedelta(days=7)
            queryset = queryset.filter(publish__gte=start_date)
        elif period == 'month':
            start_date = timezone.localtime().date() - timezone.timedelta(days=30)
            queryset = queryset.filter(publish__gte=start_date)
        elif period == 'year':
            current_year = timezone.localtime().year
            queryset = queryset.filter(publish__year=current_year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        query_string = urlencode(query_params)

        if query_string:
            query_string = '&' + query_string

        context['query_string'] = query_string
        return context
