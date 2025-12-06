from rest_framework import serializers

from users.models import User


class UserUpdateSerializer(serializers.ModelSerializer):
    def validate_user_bg(self, value):
        if value and "cloudinary.com" not in value:
            raise serializers.ValidationError("Imagem inválida")
        return value

    class Meta:
        model = User
        fields = [
            "bio",
            "avatar",
            "user_bg",
            "website",
            "location",
        ]
