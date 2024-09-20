from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import accounts as accounts_views
from api.views import movies as movies_views

app_name = 'api'

urlpatterns = [
    # Movies
    path('movies/', movies_views.MovieListAPIView.as_view(), name='api_movies_list'),

    # Accounts
    path('accounts/', accounts_views.UserListAPIView.as_view(), name='api_user_create'),
    path('accounts/activate/', accounts_views.UserActivateAPIView.as_view(), name='api_user_activate'),
    path('accounts/current/', accounts_views.CurrentUserAPIView.as_view(), name='api_user_current'),
    # path('accounts/token/', accounts_views.AccessTokenCreateAPIView.as_view(), name='api_token_create'),
    path('accounts/<int:user_id>/profile/',
         accounts_views.ProfileCreateAPIView.as_view(),
         name='user_profile_create'),

    # JWT Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
