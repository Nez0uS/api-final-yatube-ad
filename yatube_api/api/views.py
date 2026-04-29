from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import filters  # добавь в начало файла
from rest_framework import viewsets, permissions, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group
from .serializers import (
    PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
)
from .permissions import IsAuthorOrReadOnly

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для постов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для групп (только чтение)."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = None


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Вьюсет для подписок (только список и создание)."""
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    # Добавь эти строки для поиска
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']
    pagination_class = None

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
