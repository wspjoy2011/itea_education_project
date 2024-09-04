from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('activate/<str:username>/<str:token>/', views.ActivateAccountView.as_view(), name='activate'),
    path('create-profile/', views.ProfileCreateView.as_view(), name='profile_create')
]
