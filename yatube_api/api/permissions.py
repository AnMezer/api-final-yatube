from typing import TYPE_CHECKING

from rest_framework import permissions

if TYPE_CHECKING:
    from rest_framework.request import Request
    from rest_framework.views import APIView

    from posts.models import Post


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Авторизованные пользователи могут изменять только те объекты,
    автором которых являются.
    """
    def has_object_permission(self, request: 'Request',
                              view: 'APIView', obj: 'Post') -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
