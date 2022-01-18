import textwrap

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Follow, Group, Post, User
from yatube_api.settings import DATETIME_FORMAT


class GroupDetailSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Group',
    используется при просмотре группы по ID.
    """
    class Meta:
        model = Group
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Group',
    используется при просмотре групп списком.
    """
    class Meta:
        model = Group
        fields = ('id', 'title')


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Post',
    используется при работе с одним постом.
    """
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False
    )
    group_info = GroupSerializer(
        read_only=True,
        source='group'
    )
    pub_date = serializers.DateTimeField(
        read_only=True,
        format=DATETIME_FORMAT
    )

    class Meta:
        fields = (
            'id', 'author',
            'text', 'pub_date',
            'group', 'group_info',
            'comments'
        )
        read_only_fields = ('author', 'group_info', 'pub_date', 'comments')
        model = Post

    def validate_text(self, value):
        """Валидирует текст поста, он не должен быть пустым."""
        if not value:
            raise serializers.ValidationError(
                'Невозможно опубликовать пустой пост.'
            )
        return value


class PostSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Post',
    используется при работе со списком постов.
    """
    text = serializers.SerializerMethodField()
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False
    )
    group_info = GroupSerializer(
        read_only=True,
        source='group'
    )
    comments = serializers.SerializerMethodField(required=False)
    pub_date = serializers.DateTimeField(
        read_only=True,
        format=DATETIME_FORMAT
    )

    class Meta:
        fields = (
            'id', 'author',
            'text', 'pub_date',
            'group', 'group_info',
            'comments'
        )
        read_only_fields = ('author', 'group_info', 'pub_date', 'comments')
        model = Post

    def get_text(self, obj):
        """Сжимает текст до 100 символов при выводе постов списком."""
        text = obj.text
        return textwrap.shorten(text, width=100)

    def get_comments(self, obj):
        """Отображает количество комментариев к каждому посту."""
        return obj.comments.all().count()

    def validate_text(self, value):
        """Валидирует текст поста, он не должен быть пустым."""
        if not value:
            raise serializers.ValidationError(
                'Невозможно опубликовать пустой пост.'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """
    Обслуживаниет модель 'Comment',
    дает возможность управлять комментариями к постам.
    """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    created = serializers.DateTimeField(
        read_only=True,
        format=DATETIME_FORMAT
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'created', 'post')
        model = Comment

    def validate_text(self, value):
        """Валидирует текст комментария, он не должен быть пустым."""
        if not value:
            raise serializers.ValidationError(
                'Невозможно опубликовать пустой комментарий.'
            )
        return value


class FollowSerializer(serializers.ModelSerializer):
    """
    Обслуживаниет модель 'Follow'
    - реализация подписки/отписки на авторов.
    """
    user = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )
    following_posts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('id', 'user', 'following', 'following_posts')
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Такая подписка уже есть.'
            )
        ]

    def get_following_posts(self, obj):
        """Выводит количество публикаций подписки."""
        following = obj.following
        following_posts = following.posts.all().count()
        return following_posts

    def validate_following(self, value):
        """Проверяет и запрещает подписку на самого себя."""
        current_user = self.context.get('request').user
        username = current_user.username.lower()
        following = value.username.lower()
        if username == following:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя.'
            )
        return value
