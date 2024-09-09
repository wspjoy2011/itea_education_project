from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<int:post_id>/add-comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('<int:year>/<int:month>/<int:day>/<slug:post_slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:post_slug>/update/', views.PostUpdateGenericView.as_view(), name='post_update'),
    path('post/<slug:post_slug>/delete/', views.PostDeleteGenericView.as_view(), name='post_delete'),
    path('comment/<int:comment_id>/like/', views.LikeView.as_view(), name='like_comment'),
    path('comment/<int:comment_id>/dislike/', views.DislikeView.as_view(), name='dislike_comment'),
]
