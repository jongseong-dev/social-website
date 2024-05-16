import pytest

from images.forms import ImageCreateForm
from images.models import Image


@pytest.fixture
def image_form_data():
    return {
        "title": "Test Image",
        "url": "http://example.com/image.jpg",
        "description": "This is a test image",
    }


def image_create_form_with_valid_data(image_form_data):
    form = ImageCreateForm(data=image_form_data)
    assert form.is_valid()


def image_create_form_with_invalid_url(image_form_data):
    image_form_data["url"] = "http://example.com/image.txt"
    form = ImageCreateForm(data=image_form_data)
    assert not form.is_valid()


def image_create_form_save(image_form_data):
    form = ImageCreateForm(data=image_form_data)
    if form.is_valid():
        image = form.save()
        assert isinstance(image, Image)
        assert image.title == image_form_data["title"]
        assert image.description == image_form_data["description"]


def image_create_form_save_with_commit_false(image_form_data):
    form = ImageCreateForm(data=image_form_data)
    if form.is_valid():
        image = form.save(commit=False)
        assert isinstance(image, Image)
        assert image.title == image_form_data["title"]
        assert image.description == image_form_data["description"]
        assert not Image.objects.filter(id=image.id).exists()
