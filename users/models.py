from django.contrib.auth.models import AbstractUser
from django.db import models


def user_avatar_path(instance, filename):
    return f"avatars/{instance.pk or 'temp'}/{filename}"


class User(AbstractUser):
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("USER", "User"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")

    user_tag = models.CharField(max_length=30, unique=True, default="@NewUser", blank=True)

    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True, null=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        if not self.user_tag:
            base = f"@{self.username}"
            tag = base
            counter = 1
            while User.objects.filter(user_tag=tag).exists():
                tag = f"{base}{counter}"
                counter += 1
            self.user_tag = tag
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
