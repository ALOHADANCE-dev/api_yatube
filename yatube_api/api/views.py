from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets

from posts.models import Comment, Group, Post
from .permission import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)

    def get_post(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post

    def get_queryset(self):
        post = self.get_post()
        return post.comments

    def perform_create(self, serializer):
        post = self.get_post()
        serializer.save(author=self.request.user, post=post)
