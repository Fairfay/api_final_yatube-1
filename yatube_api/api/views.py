from django.shortcuts import get_object_or_404
from rest_framework import filters, pagination, permissions, viewsets

from posts.models import Follow, Group, Post

from .permissions import FollowObjectPermission, IsOwnerOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer,
                          GroupDetailSerializer, GroupSerializer,
                          PostDetailSerializer, PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    Обработка запросов к постам.
    """
    queryset = Post.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = pagination.LimitOffsetPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return PostSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Обработка запросов к группам.
    """
    queryset = Group.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupSerializer
        return GroupDetailSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    Обработка запросов к комментариям.
    """
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_post(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post

    def get_queryset(self):
        post = self.get_post()
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_post()
        )


class FollowViewSet(viewsets.ModelViewSet):
    """
    Обработка запросов к подпискам.
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        FollowObjectPermission
    )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        queryset = user.follower.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
