from django.contrib.auth import get_user_model
from rest_framework import serializers

from follows.models import Follow

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "full_name",
            "role",
            "user_tag",
            "bio",
            "avatar",
            "user_bg",
            "website",
            "location",
            "is_verified",
            "date_joined",
            "followers_count",
            "following_count",
        ]
        read_only_fields = [
            "id",
            "email",
            "is_verified",
            "date_joined",
            "user_tag",
            "followers_count",
            "following_count",
        ]

    def get_followers_count(self, obj):
        return Follow.objects.filter(following=obj).count()

    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj).count()


def validate_username(self, value):
    if User.objects.exclude(pk=self.instance.pk).filter(username=value).exists():
        raise serializers.ValidationError("Esse username já está em uso.")

    if not value[0].isupper():
        raise serializers.ValidationError("O username deve começar com letra maiúscula.")

    return value
