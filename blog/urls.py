from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('hello/<int:user_id>/', views.hello, name='hello')
]
