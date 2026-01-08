from typing import TYPE_CHECKING, Any

from django.shortcuts import get_object_or_404

from posts.models import Post

if TYPE_CHECKING:
    from rest_framework.request import Request
    from rest_framework.serializers import Serializer


class AuthorFromRequestMixin:
    """Миксин для создания постов.

    Автор устанавливается автоматически из запроса.
    """
    request: 'Request'
    kwargs: dict[str, Any]

    def perform_create(self, serializer: 'Serializer') -> None:
        serializer.save(author=self.request.user)


class AuthorPostFromRequestMixin:
    """Миксин для создания комментариев к постам.

    Автор и пост устанавливается автоматически из запроса.
    """
    request: 'Request'
    kwargs: dict[str, Any]

    def get_post(self) -> Post:
        """Возвращает пост с id из запроса"""
        return get_object_or_404(Post, id=self.kwargs['post_pk'])

    def perform_create(self, serializer: 'Serializer') -> None:
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)


class UserFromRequestMixin:
    """Миксин для создания подписок.

    user устанавливается автоматически из запроса.
    """
    request: 'Request'
    kwargs: dict[str, Any]

    def perform_create(self, serializer: 'Serializer') -> None:
        serializer.save(user=self.request.user)
