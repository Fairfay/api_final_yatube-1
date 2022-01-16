from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from posts.models import Group, Post, Comment, Follow
from .permissions import FollowPermission
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer, GroupDetailSerializer


User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    """Запрос к постам."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Запрос к группам."""
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return GroupSerializer
        return GroupDetailSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, FollowPermission)

    def get_queryset(self):
        user = self.request.user
        queryset = user.follower.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
