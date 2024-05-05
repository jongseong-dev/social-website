import factory
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
