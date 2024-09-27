from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Category, Post, Comment

User = get_user_model()


class AuthorReadSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['pk', 'full_name', 'username']

    def get_full_name(self, obj: User):
        return obj.get_full_name()


class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PostReadSerializer(serializers.ModelSerializer):
    category = CategoryReadSerializer(read_only=True)
    author = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_author(self, obj):
        return AuthorReadSerializer(obj.author).data

    def get_likes(self, obj):
        return AuthorReadSerializer([like.user for like in obj.likes.all()], many=True).data

    def get_dislikes(self, obj):
        return AuthorReadSerializer([dislike.user for dislike in obj.dislikes.all()], many=True).data

    def get_likes_count(self, obj):
        return obj.likes_count()

    def get_dislikes_count(self, obj):
        return obj.dislikes_count()


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Post
        fields = ['title', 'body', 'category']


class CommentReadSerializer(serializers.ModelSerializer):
    author = AuthorReadSerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_likes(self, obj):
        return obj.likes_count()

    def get_dislikes(self, obj):
        return obj.dislikes_count()



















