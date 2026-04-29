from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('id', 'author', 'created', 'post')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        # id readOnly, остальные обязательные: title, slug, description
        fields = ('id', 'title', 'slug', 'description')
        read_only_fields = ('id',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        following = attrs['following']

        # подписка на самого себя — ошибка
        if user == following:
            raise serializers.ValidationError({
                'following': 'Нельзя подписаться на самого себя!'
            })

        # уже есть такая подписка — ошибка
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError({
                'following': 'Вы уже подписаны на этого пользователя.'
            })

        return attrs
