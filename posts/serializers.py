from rest_framework import serializers

from users.serializers.publicSerializer import UserPublicSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    image = serializers.URLField(required=False, allow_null=True)
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "image",
            "is_liked",
            "created_at",
            "likes_count",
            "comments_count",
        ]
        read_only_fields = [
            "id",
            "author",
            "created_at",
            "likes_count",
            "comments_count",
        ]

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False
