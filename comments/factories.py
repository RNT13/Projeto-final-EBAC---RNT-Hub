import factory

from comments.models import Comment
from posts.factories import PostFactory
from users.factories import UserFactory


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory(UserFactory)
    post = factory.SubFactory(PostFactory)
    text = factory.Faker("sentence")
