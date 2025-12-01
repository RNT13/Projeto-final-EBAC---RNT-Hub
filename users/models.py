from django.contrib.auth.models import AbstractUser
from django.db import models


def user_avatar_path(instance, filename):
    return f"avatars/{instance.pk or 'temp'}/{filename}"


class User(AbstractUser):
    email = models.EmailField(unique=True)

    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
