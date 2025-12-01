from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from comments.permissions import IsOwnerOrReadOnly
from posts.models import Post

from .models import Comment
from .serializers import CommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id).order_by("-created_at")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        serializer.save(user=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        return Comment.objects.filter(post_id=post_id)
