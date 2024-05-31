import datetime

import factory
import factory.fuzzy
from django.contrib.auth.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda a: f"{a.username}@example.com")

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        instance.set_password(instance.password)
        instance.save()


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "account.Profile"

    user = factory.SubFactory(UserFactory)
    date_of_birth = factory.fuzzy.FuzzyDate(
        datetime.date(1990, 1, 1),
        datetime.date(2000, 12, 31),
    )
    photo = factory.django.ImageField(filename="test.jpg")


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "account.Contact"

    user_from = factory.SubFactory(UserFactory)
    user_to = factory.SubFactory(UserFactory)
