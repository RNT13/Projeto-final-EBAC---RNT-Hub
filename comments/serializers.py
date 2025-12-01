from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    post_id = serializers.IntegerField(source="post.id", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "username", "post_id", "content", "created_at"]
        read_only_fields = ["id", "created_at", "user", "post_id"]
