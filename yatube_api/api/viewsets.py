from rest_framework import mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsOwnerOrReadOnly


class BaseViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет.

    Устанавливает:
                - доступ для чтения всем.
                - доступ для изменения только автору.
                - пагинация по условиям из запроса.
    """
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """Базовый вьюсет.

    Доступны запросы:
                    - POST
                    - GET
    """
