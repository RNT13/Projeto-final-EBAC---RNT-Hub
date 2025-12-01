import factory

from likes.models import Like
from posts.factories import PostFactory
from users.factories import UserFactory


class LikeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Like

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
