# type: ignore
import factory.django

from images.models import Image


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    title = factory.Faker("sentence", nb_words=3)
    url = factory.Faker("url")
    user = factory.SubFactory("account.factory.UserFactory")
    description = factory.Faker("text")
    created = factory.Faker("date_time_this_year")
    image = factory.django.ImageField(filename="test.jpg")
    users_like = factory.RelatedFactory("account.factory.UserFactory")
