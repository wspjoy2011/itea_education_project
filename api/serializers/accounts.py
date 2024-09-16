from django.contrib.auth import get_user_model, authenticate
from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from accounts.validators import validate_password_strength, validate_file_size
from accounts.models import APIToken, Profile

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password_strength]
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data, is_active=False)
        return user


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name']


class UserActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField(max_length=64)


class AccessTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid login credentials")

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        APIToken.objects.filter(user=user).delete()
        access_token = APIToken.objects.create(user=user)
        return access_token


class ProfileCreateSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(
        choices=Profile.GENDER_CHOICES,
        error_messages={
            'invalid_choice': 'Wrong choice. Valid options are: m or f'
        }
    )
    avatar = serializers.ImageField(
        required=True,
        validators=[
            validate_file_size,
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ]
    )

    class Meta:
        model = Profile
        fields = ['avatar', 'gender', 'date_of_birth', 'info']


class ProfileReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'





















