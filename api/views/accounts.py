from django.contrib.auth import get_user_model
from django.db import transaction
from django.urls import reverse
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from accounts.models import APIToken
from accounts.services import AccountsEmailNotification
from api.authentication import TokenAuthentication
from api.serializers.accounts import (
    AccessTokenSerializer,
    UserCreateSerializer,
    UserReadSerializer,
    UserActivationSerializer,
    ProfileReadSerializer,
    ProfileCreateSerializer
)
from api.pagination import CustomPagination

User = get_user_model()


class UserListAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get_authenticators(self):
        if hasattr(self, 'request') and self.request and self.request.method == 'GET':
            return [TokenAuthentication()]
        return super().get_authenticators()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()

    def get_paginator(self, queryset, request):
        paginator = CustomPagination()
        return paginator.paginate_queryset(queryset, request), paginator

    def get(self, request: Request) -> Response:
        users = User.objects.all().order_by('username')
        paginated_users, paginator = self.get_paginator(users, request)
        serializer = UserReadSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = UserCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        activation_token = APIToken.objects.create(user=user)

        activate_url = (f'{self.request.scheme}://{self.request.get_host()}'
                        f'{reverse("accounts:activate", args=[user.username, activation_token.token])}')

        AccountsEmailNotification().send_activation_email(
            email=user.email,
            full_name=user.get_full_name(),
            activation_url=activate_url
        )

        serializer_data = UserReadSerializer(user).data
        return Response({
            'user': serializer_data,
            "message": f"User registration successfully. Please check your email {user.email} for next steps"
        }, status=status.HTTP_201_CREATED)


class UserActivateAPIView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserActivationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        token = serializer.validated_data['token']

        activation_token = get_object_or_404(APIToken, user__email=email, token=token)

        if not activation_token.verify_token():
            return Response({
                "error": "Activation token expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            activation_token.user.is_active = True
            activation_token.user.save()
            activation_token.delete()

        return Response({
            "message": "Activation complete"
        }, status=status.HTTP_201_CREATED)


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user
        serializer = UserReadSerializer(user)
        return Response({
            "results": serializer.data
        }, status=status.HTTP_200_OK)


class AccessTokenCreateAPIView(APIView):
    authentication_classes = []

    def post(self, request: Request) -> Response:
        serializer = AccessTokenSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        access_token = serializer.save()
        return Response({
            "results": access_token.token
        }, status=status.HTTP_201_CREATED)


class ProfileCreateAPIView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, user_id: int) -> Response:
        if user_id != request.user.id:
            return Response({
                "error": "You can't create profile for this user"
            }, status=status.HTTP_403_FORBIDDEN)

        if hasattr(request.user, 'profile'):
            return Response({
                "error": "Profile already exists"
            }, status=status.HTTP_400_BAD_REQUEST)

        create_serializer = ProfileCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            return Response({
                "errors": create_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        profile = create_serializer.save(user=request.user)
        read_serializer = ProfileReadSerializer(profile)

        return Response({
            "message": f"User {request.user.username} profile created",
            "data": read_serializer.data
        }, status=status.HTTP_201_CREATED)
