from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


def user_avatar_path(instance, filename):
    return f"avatars/{instance.pk or 'temp'}/{filename}"


class User(AbstractUser):
    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=100, blank=True)

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9._-]+$", message='Username pode conter apenas letras, números, ".", "_" e "-".'
            )
        ],
    )

    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("USER", "User"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")

    user_tag = models.CharField(max_length=20, unique=True, blank=True)

    bio = models.TextField(blank=True)
    avatar = models.URLField(blank=True, null=True)
    user_bg = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    REQUIRED_FIELDS = ["username", "full_name"]

    def save(self, *args, **kwargs):
        if not self.pk:
            # criação
            base = f"@{self.username}"
        else:
            old = User.objects.filter(pk=self.pk).values_list("username", flat=True).first()
            if old != self.username:
                base = f"@{self.username}"
            else:
                super().save(*args, **kwargs)
                return

        tag = base
        counter = 1
        while User.objects.filter(user_tag=tag).exclude(pk=self.pk).exists():
            tag = f"{base}{counter}"
            counter += 1

        self.user_tag = tag
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
