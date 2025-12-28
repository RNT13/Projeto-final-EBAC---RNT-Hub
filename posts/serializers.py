from rest_framework import serializers

from users.serializers.publicSerializer import UserPublicSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    image = serializers.URLField(required=False, allow_null=True, allow_blank=True)
    is_liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

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
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        return obj.likes.filter(user=request.user).exists()

    def validate(self, data):
        content = data.get("content")
        image = data.get("image")

        if image == "":
            data["image"] = None

        if not content and not image:
            raise serializers.ValidationError("O post precisa ter texto ou imagem.")

        return data
