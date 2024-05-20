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
def client():
    return Client()


@pytest.fixture
def login(user, plain_password, client):
    client.login(username=user.username, password=plain_password)


@pytest.mark.django_db
def test_image_create_with_valid_data(login, client, create_url):
    response = client.post(
        create_url,
        data={"title": "New Image", "url": "http://example.com/new.jpg"},
    )

    assert response.status_code == 302
    assert "Image added successfully" in [
        str(m) for m in list(response.wsgi_request._messages)
    ]


@pytest.mark.django_db
def test_image_create_with_invalid_data(login, client, create_url):
    response = client.post(
        create_url, data={"title": "", "url": "http://example.com/new.jpg"}
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_image_detail_with_existing_image(login, image, client):
    response = client.get(f"/images/detail/{image.id}/{image.slug}/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_image_detail_with_nonexistent_image(login, client):
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
