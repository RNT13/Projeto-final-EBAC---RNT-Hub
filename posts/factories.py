import factory

from posts.models import Post
from users.factories import UserFactory


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    author = factory.SubFactory(UserFactory)
    content = "Post de teste"
