from typing import TYPE_CHECKING, Union

from rest_framework import permissions

if TYPE_CHECKING:
    from django.contrib.auth.models import AnonymousUser, User
    from rest_framework.request import Request
    from rest_framework.views import APIView

    from posts.models import Post


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Разрешает анонимным пользователям только безопасные методы.

    Авторизованные пользователи могут изменять только те объекты,
    автором которых являются.
    """
    def has_permission(self, request: 'Request', view: 'APIView') -> bool:
        user: Union['User', 'AnonymousUser'] = request.user
        return (request.method in permissions.SAFE_METHODS
                or user.is_authenticated)

    def has_object_permission(self, request: 'Request',
                              view: 'APIView', obj: 'Post') -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
