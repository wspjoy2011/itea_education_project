from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, FormView, UpdateView, DeleteView

from .forms import CommentForm, PostForm
from .models import Post, Comment, CommentLike, CommentDislike
from .mixins import PostPermissionMixin


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
    form_comment = CommentForm()
    context = {
        'post': post,
        'form': form_comment
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


class AddCommentView(LoginRequiredMixin, FormView):
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        if request.method != 'POST':
            return HttpResponseNotAllowed(['POST'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        new_comment = form.save(commit=False)
        new_comment.post = post
        new_comment.author = self.request.user
        new_comment.save()
        return HttpResponseRedirect(f'{new_comment.post.get_absolute_url()}#commentLike{new_comment.pk}')


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if comment.is_liked_by(request.user):
        like = comment.likes.get(user=request.user)
        like.delete()
    else:
        CommentLike.objects.create(comment=comment, user=request.user)
        if comment.is_disliked_by(request.user):
            dislike = comment.dislikes.get(user=request.user)
            dislike.delete()
    return HttpResponseRedirect(f'{comment.post.get_absolute_url()}#commentLike{comment.pk}')


class LikeView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.is_liked_by(request.user):
            like = comment.likes.get(user=request.user)
            like.delete()
        else:
            CommentLike.objects.create(comment=comment, user=request.user)
            if comment.is_disliked_by(request.user):
                dislike = comment.dislikes.get(user=request.user)
                dislike.delete()
        return HttpResponseRedirect(f'{comment.post.get_absolute_url()}#commentLike{comment.pk}')


class DislikeView(LoginRequiredMixin, View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)

        if comment.is_disliked_by(request.user):
            dislike = comment.dislikes.get(user=request.user)
            dislike.delete()
        else:
            CommentDislike.objects.create(comment=comment, user=request.user)
            if comment.is_liked_by(request.user):
                like = comment.likes.get(user=request.user)
                like.delete()
        return HttpResponseRedirect(f'{comment.post.get_absolute_url()}#commentLike{comment.pk}')


class PostUpdateView(LoginRequiredMixin, PostPermissionMixin,View):
    def get(self, request, post_slug):
        post = self.get_post_by_slug(post_slug)
        form = PostForm(instance=post)
        context = {'post': post, 'form': form}
        return render(request, 'blog/post/update.html', context)

    def post(self, request, post_slug):
        post = self.get_post_by_slug(post_slug)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            return redirect(post.get_absolute_url())
        else:
            context = {'post': post, 'form': form}
            return render(request, 'blog/post/update.html', context)


class PostUpdateGenericView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post/update.html'
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        if not request.user.is_superuser and not request.user == post.author:
            return HttpResponseForbidden("Ypu don't have permission to delete this post")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        post_slug = self.kwargs.get('post_slug')
        return get_object_or_404(Post, slug=post_slug)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.slug = slugify(post.title)
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


class PostDeleteView(LoginRequiredMixin, PostPermissionMixin, View):
    def post(self, request, post_slug):
        post = self.get_post_by_slug(post_slug)
        post.delete()
        messages.info(request, 'Post deleted')
        return redirect('blog:post_list')


class PostDeleteGenericView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post/confirm_delete.html'
    context_object_name = 'post'
    success_url = reverse_lazy('blog:post_list')
    
    def dispatch(self, request, *args, **kwargs):
        post = self.get_object()

        if not request.user.is_superuser and not request.user == post.author:
            return HttpResponseForbidden("You don't have permission to delete this post")

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        post_slug = self.kwargs.get('post_slug')
        return get_object_or_404(Post, slug=post_slug)
    
    def delete(self, request, *args, **kwargs):
        messages.info(request, 'Post deleted')
        return super().delete(request, *args, **kwargs)















