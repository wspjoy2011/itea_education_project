from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.filters import PostFilter
from api.serializers.blog import PostReadSerializer, PostCreateSerializer, CommentReadSerializer
from blog.models import Post
from api.permissions import IsAuthorOrReadOnly


class PostListCreateAPIView(generics.ListCreateAPIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all().select_related('category')
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter

    def get_authenticators(self):
        if self.request.method not in SAFE_METHODS:
            return [JWTAuthentication()]
        return super().get_authenticators()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostReadSerializer
        return PostCreateSerializer

    def create(self, request, *args, **kwargs):
        create_serializer: PostCreateSerializer = self.get_serializer(data=request.data)
        create_serializer.is_valid(raise_exception=True)
        user = self.request.user
        post = create_serializer.save(author=user, status='p')
        read_serializer = PostReadSerializer(post)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class PostRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.published.all().select_related('category')
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostReadSerializer
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        read_serializer = PostReadSerializer(self.get_object())
        return Response(read_serializer.data)


class CommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = CommentReadSerializer
    authentication_classes = []

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()



















