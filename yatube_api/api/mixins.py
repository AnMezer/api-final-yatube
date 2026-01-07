from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from rest_framework.request import Request

    from .serializers import (
        CommentSerializer,
        FollowSerializer,
        PostSerializer,
    )


class AuthorFromRequestMixin:
    """Миксин для создания постов.

    Автор устанавливается автоматически из запроса.
    """
    request: 'Request'
    kwargs: dict[str, Any]

    def perform_create(self, serializer: 'PostSerializer') -> None:
        serializer.save(author=self.request.user)


class AuthorPostFromRequestMixin:
    """Миксин для создания комментариев к постам.

    Автор и пост устанавливается автоматически из запроса.
    """
    request: 'Request'
    kwargs: dict[str, Any]

    def perform_create(self, serializer: 'CommentSerializer') -> None:
        serializer.save(author=self.request.user,
                        post_id=self.kwargs['post_pk'])


class UserFromRequestMixin:
    """Миксин для создания подписок.

    user устанавливается автоматически из запроса.
    """
    request: 'Request'
    kwargs: dict[str, Any]

    def perform_create(self, serializer: 'FollowSerializer') -> None:
        serializer.save(user=self.request.user)
