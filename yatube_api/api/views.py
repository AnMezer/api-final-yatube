from typing import TYPE_CHECKING

from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from posts.models import Comment, Group, Post

from .mixins import (
    AuthorFromRequestMixin,
    AuthorPostFromRequestMixin,
    UserFromRequestMixin,
)
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)
from .viewsets import BaseViewSet, CreateListViewSet

if TYPE_CHECKING:
    from django.db.models import Manager

    from posts.models import Follow

    class User:
        follower: Manager[Follow]
        following: Manager[Follow]


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
        post = get_object_or_404(Post, id=self.kwargs['post_pk'])
        return post.comments.all()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для работы с группами.

    Доступен для чтения всем пользователям.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination


class FollowViewSet(UserFromRequestMixin, CreateListViewSet):
    """Вьюсет для работы с подписками.

    Доступен только авторизованным пользователям.
    """
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user: User = self.request.user
        return user.follower.all()
