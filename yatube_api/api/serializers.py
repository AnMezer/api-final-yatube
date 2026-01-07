from rest_framework import serializers

from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов.

    Поля:
        Все поля из модели Post.
        author - username текущего пользователя.
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        fields = '__all__'
        model = Post
        read_only_fields = ('pub_date', 'id')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев.

    Поля:
        Все поля из модели Comment.
        author - username текущего пользователя.
    """
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    post = serializers.IntegerField(source='post_id', read_only=True)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
        read_only_fields = ('created', 'id')


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для сообществ.

    Поля:
        Все поля из модели Group.
    """

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок.

    Поля:
        user - username текущего пользователя.
        following - username пользователя, на которого оформляется подписка.
    """
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(slug_field='username',
                                             queryset=User.objects.all())

    class Meta:
        fields = ('user', 'following')
        model = Follow
        read_only_fields = ('id',)

    def validate_following(self, value):
        """Проверяет корректность подписки.

        Args:
            value: Валидированное значение поля following

        Raises:
            serializers.ValidationError:
                                    - При попытке подписаться на самого себя.
                                    - При попытке повторной подписки.

        Returns:
            Исходные данные.
        """
        user = self.context['request'].user
        if user == value:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.')
        if Follow.objects.filter(user=user, following=value).exists():
            raise serializers.ValidationError(
                f'Вы уже подписаны на {value}.')
        return value
