import textwrap
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
# "token": "fc8c13b5652f666d529af6ba4d9f83244581f30e"
from django.contrib.auth import get_user_model
from posts.models import Group, Post, Comment, Follow
from yatube_api.settings import DATETIME_FORMAT


User = get_user_model()


class GroupDetailSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Group',
    используется при просмотре группы.
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
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = GroupSerializer(required=False)
    group_id = serializers.IntegerField(required=False, write_only=True)
    pub_date = serializers.DateTimeField(required=False, format=DATETIME_FORMAT)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'group', 'group_id', 'comments')
        read_only_fields = ('author', 'pub_date', 'comments')
        model = Post

    def validate_text(self, value):
        """Валидирует текст поста, он не должен быть пустым."""
        if not value:
            raise serializers.ValidationError(
                'Невозможно опубликовать пустой пост!'
            )
        return value


class PostSerializer(serializers.ModelSerializer):
    """
    Обслуживает модель 'Post',
    используется при работе со списком постов.
    """
    text = serializers.SerializerMethodField()
    author = SlugRelatedField(slug_field='username', read_only=True)
    group = GroupSerializer(required=False)
    group_id = serializers.IntegerField(required=False, write_only=True)
    comments = serializers.SerializerMethodField(required=False)
    pub_date = serializers.DateTimeField(required=False, format=DATETIME_FORMAT)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'group', 'group_id', 'comments')
        read_only_fields = ('author', 'pub_date', 'comments')
        model = Post

    def get_text(self, obj):
        """Сжимает текст до 100 символов при выводе постов списком."""
        text = obj.text
        return textwrap.shorten(text, width=100)

    def get_comments(self, obj):
        """Отображает количество комментариев у каждого поста."""
        return obj.comments.all().count()

    def validate_text(self, value):
        """Валидирует текст поста, он не должен быть пустым."""
        if not value:
            raise serializers.ValidationError(
                'Невозможно опубликовать пустой пост!'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для обслуживания модели 'Comment',
    дает возможность управлять комментариями к постам.
    """
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    created = serializers.DateTimeField(required=False, format=DATETIME_FORMAT)

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'created', 'post')
        model = Comment

    def validate_text(self, value):
        """Валидирует текст комментария, он не должен быть пустым."""
        if not value:
            raise serializers.ValidationError(
                'Невозможно опубликовать пустой пост!'
            )
        return value


class FollowSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для обслуживания модели 'Follow'
    - подписки/отписки на авторов.
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

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Такая подписка уже есть.'
            )
        ]

    def validate_following(self, value):
        current_user = self.context.get('request').user
        username = current_user.username.lower()
        following = value.username.lower()
        if username == following:
            raise serializers.ValidationError(
                'Нельзя подписываться на самого себя.'
            )
        return value
