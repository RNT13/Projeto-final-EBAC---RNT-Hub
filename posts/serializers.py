from rest_framework import serializers

from users.serializers.publicSerializer import UserPublicSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserPublicSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "image",
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

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
