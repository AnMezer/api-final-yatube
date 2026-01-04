from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from posts.models import Comment, Follow, Group, Post

from .mixins import (
    AuthorFromRequestMixin,
    AuthorPostFromRequestMixin,
    UserFromRequestMixin,
)
from .permissions import OwnerOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    """Базовый вьюсет.

    Устанавливает:
                - доступ для чтения всем.
                - доступ для изменения только автору.
                - пагинация по условиям из запроса.
    """
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination


class PostViewSet(AuthorFromRequestMixin, BaseViewSet):
    """Вьюсет для работы с постами.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(AuthorPostFromRequestMixin, BaseViewSet):
    """Вьюсет для работы с комментариями.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с группами.

    Доступен для чтения всем пользователям.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination


class FollowViewSet(UserFromRequestMixin, viewsets.ModelViewSet):
    """Вьюсет для работы с подписками.

    Доступен только авторизованным пользователям.
    """
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
