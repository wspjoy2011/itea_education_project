from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<str:username>/<str:token>/', views.ActivateAccountView.as_view(), name='activate')
]
