from unittest.mock import patch

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import Client
from django.urls import reverse

from account.factory import UserFactory
from images.factory import ImageFactory


@pytest.fixture
def create_url():
    return reverse("images:create")


@pytest.fixture
def like_url():
    return reverse("images:like")


@pytest.fixture
def plain_password():
    return "testpassword"


@pytest.fixture
def user(plain_password):
    return UserFactory.create(
        username="test", email="test@example.com", password=plain_password
    )


@pytest.fixture
def image(user):
    return ImageFactory.create(
        user=user,
        title="Test Image",
        url="http://example.com/image.jpg",
        slug="test-image",
    )


@pytest.fixture
def images(user):
    return ImageFactory.create_batch(10)


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def login(user, plain_password, client):
    client.login(username=user.username, password=plain_password)


@pytest.mark.django_db
@patch("images.forms.ImageCreateForm.save")
def test_image_create_with_valid_data(mock, login, client, create_url):
    mock.return_value = ImageFactory.build()
    response = client.post(
        create_url,
        data={"title": "New Image", "url": "http://example.com/new.jpg"},
    )
    assert response.status_code == 302
    assert "Image added successfully" in [
        str(m) for m in list(response.wsgi_request._messages)
    ]


@pytest.mark.django_db
def test_image_create_with_invalid_title(login, client, create_url):
    response = client.post(
        create_url, data={"title": "", "url": "http://example.com/new.png"}
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_image_create_with_invalid_url(login, client, create_url):
    response = client.post(
        create_url,
        data={"title": "Invalid Url", "url": "http://example.com/new.oo"},
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_image_create_with_invalid_download(login, client, create_url):
    response = client.post(
        create_url,
        data={
            "title": "Invalid Download",
            "url": "http://example.com/new-test-image.png",
        },
    )

    assert response.status_code == 200
    assert "Could not download the image." in response.content.decode()


@pytest.mark.django_db
@patch("redis.Redis")
def test_image_detail_with_existing_image(mock, login, image, client):
    response = client.get(f"/images/detail/{image.id}/{image.slug}/")

    assert response.status_code == 200


@pytest.mark.django_db
@patch("redis.Redis")
def test_image_detail_with_nonexistent_image(mock, login, client):
    response = client.get("/images/detail/9999/nonexistent/")

    assert response.status_code == 404


@pytest.mark.django_db
def test_image_like_with_valid_data(login, image, client, like_url):
    response = client.post(like_url, data={"id": image.id, "action": "like"})

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_image_like_with_invalid_action(login, image, client, like_url):
    response = client.post(
        like_url, data={"id": image.id, "action": "invalid"}
    )

    assert response.status_code == 200
    assert response.json() == {"status": "error"}


@pytest.mark.django_db
def test_image_like_with_invalid_id(login, client, like_url):
    response = client.post(like_url, data={"id": 9999, "action": "like"})

    assert response.status_code == 200
    assert response.json() == {"status": "error"}


@pytest.mark.django_db
def test_image_like_without_login(image, client, like_url):
    response = client.post(like_url, data={"id": image.id, "action": "like"})
    response.user = AnonymousUser()
    assert response.status_code == 302
    assert "login" in response.url


@pytest.mark.django_db
def test_image_list_with_valid_page(login, client, images):
    response = client.get("/images/?page=1")
    assert response.status_code == 200


@pytest.mark.django_db
def test_image_list_with_invalid_page(login, client, images):
    response = client.get("/images/?page=100")
    assert response.status_code == 200


@pytest.mark.django_db
def test_image_list_with_images_only(login, client, images):
    response = client.get("/images/?images_only=true")
    assert response.status_code == 200


@pytest.mark.django_db
def test_image_list_without_login(client, images):
    response = client.get("/images/")
    assert "login" in response.url


@pytest.fixture
def ranking_url():
    return reverse("images:ranking")


@pytest.mark.django_db
@patch("redis.Redis")
def test_image_ranking_view(mock, login, images, client, ranking_url):
    response = client.get(ranking_url)
    assert response.status_code == 200


@pytest.mark.django_db
@patch("redis.Redis")
def test_image_ranking_view_without_login(mock, images, client, ranking_url):
    response = client.get(ranking_url)
    assert response.status_code == 302
    assert "login" in response.url
