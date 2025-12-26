import factory

from comments.models import Comment
from posts.factories import PostFactory


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    user = factory.SubFactory("users.factories.UserFactory")
    post = factory.SubFactory(PostFactory)
    content = factory.Faker("sentence")
