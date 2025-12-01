import factory

from notifications.models import Notification
from users.factories import UserFactory


class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    user = factory.SubFactory(UserFactory)
    text = factory.Faker("sentence")
    is_read = False
