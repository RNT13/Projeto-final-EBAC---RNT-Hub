from django.contrib.auth import get_user_model
from rest_framework import serializers

from follows.models import Follow

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField(read_only=True)
    is_follower = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "user_tag",
            "avatar",
            "is_verified",
            "is_following",
            "is_follower",
        ]

    def get_is_following(self, obj) -> bool:
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        return Follow.objects.filter(follower=request.user, following=obj).exists()

    def get_is_follower(self, obj) -> bool:
        request = self.context.get("request")

        if not request or request.user.is_anonymous:
            return False

        return Follow.objects.filter(follower=obj, following=request.user).exists()
