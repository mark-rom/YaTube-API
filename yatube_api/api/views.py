from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, permissions
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (
    CommentSerializer, FollowSerializer,
    GroupSerializer, PostSerializer
)
from .permissions import AuthorOrReadOnly, ReadOnly

from posts.models import Group, Post, Follow


class BaseTextViewSet(viewsets.ModelViewSet):
    """Base viewset for Post and Comment viewsets.
    Provides IsAuthenticatedOrReadOnly and
    AuthorOrReadOnly permissions.
    """
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorOrReadOnly
    )


class PostViewSet(BaseTextViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(BaseTextViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post.comments.all()

    def perform_create(self, serializer):
        author = self.request.user
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=author, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (ReadOnly,)


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
