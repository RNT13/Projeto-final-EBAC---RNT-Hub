import factory
from django.contrib.auth import get_user_model

from posts.factories import PostFactory

from .models import Comment

User = get_user_model()


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory("users.factories.UserFactory")
    post = factory.SubFactory(PostFactory)
    content = factory.Faker("sentence")
