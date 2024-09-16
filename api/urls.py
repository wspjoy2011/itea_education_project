from django.urls import path

from api.views import accounts as accounts_views

app_name = 'api'

urlpatterns = [
    path('accounts/', accounts_views.UserListAPIView.as_view(), name='api_user_create'),
    path('accounts/activate/', accounts_views.UserActivateAPIView.as_view(), name='api_user_activate'),
    path('accounts/current/', accounts_views.CurrentUserAPIView.as_view(), name='api_user_current'),
    path('accounts/token/', accounts_views.AccessTokenCreateAPIView.as_view(), name='api_token_create'),
]
