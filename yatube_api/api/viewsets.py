from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination

from .permissions import OwnerOrReadOnly


class BaseViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет.

    Устанавливает:
                - доступ для чтения всем.
                - доступ для изменения только автору.
                - пагинация по условиям из запроса.
    """
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """Базовый вьюсет.

    Доступны запросы:
                    - POST
                    - GET
    """
    pass
