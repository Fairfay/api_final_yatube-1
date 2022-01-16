from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
# "token": "fc8c13b5652f666d529af6ba4d9f83244581f30e"
from django.contrib.auth import get_user_model
from posts.models import Group, Post, Comment, Follow


User = get_user_model()


class GroupDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'title')


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = GroupSerializer(required=False)
    group_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        #fields = '__all__'
        fields = ('id', 'author', 'text', 'pub_date', 'group', 'group_id', 'comments')
        read_only_fields = ('author', 'comments')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        fields = '__all__'
        model = Follow
