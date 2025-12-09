from rest_framework import serializers

from users.models import User


class UserUpdateSerializer(serializers.ModelSerializer):

    def to_internal_value(self, data):
        for field in ["avatar", "user_bg", "website"]:
            if data.get(field) == "":
                data[field] = None
        return super().to_internal_value(data)

    class Meta:
        model = User
        fields = [
            "bio",
            "avatar",
            "user_bg",
            "website",
            "location",
        ]
