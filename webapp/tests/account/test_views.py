import pytest
from django.test import Client
from django.urls import reverse

from webapp.account.factory import UserFactory


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def plain_password():
    return "password"


@pytest.fixture
def user(plain_password):
    return UserFactory.create(password=plain_password)


@pytest.fixture
def dashboard_url():
    return reverse("dashboard")


@pytest.fixture
def register_url():
    return reverse("register")


@pytest.fixture
def register_user():
    return UserFactory.create(
        username="testuser", email="test@test.com", password="testpassword"
    )


@pytest.mark.django_db
def test_get_dashboard_login_user(client, user, dashboard_url, plain_password):
    client.login(username=user.username, password=plain_password)
    response = client.get(dashboard_url)
    assert response.status_code == 200
    assert "account/dashboard.html" in [
        template.name for template in response.templates
    ]


def test_dashboard_unauthenticated_user_redirect_login(client, dashboard_url):
    response = client.get(dashboard_url)
    assert response.status_code == 302
    expected_url = reverse("login") + "?next=" + dashboard_url
    assert response.url == expected_url


@pytest.mark.parametrize(
    "data, template",
    [
        (
            {
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "newpassword",
                "password2": "newpassword",
            },
            "account/register_done.html",
        ),
        (
            {
                "username": "",
                "email": "newuser@test.com",
                "password": "newpassword",
                "password2": "newpassword",
            },
            "account/register.html",
        ),
        (
            {
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "",
                "password2": "newpassword",
            },
            "account/register.html",
        ),
        (
            {
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "newpassword",
                "password2": "wrongpassword",
            },
            "account/register.html",
        ),
        (
            {
                "username": "newuser",
                "email": "invalidemail",
                "password": "newpassword",
                "password2": "newpassword",
            },
            "account/register.html",
        ),
    ],
)
@pytest.mark.django_db
def test_register_form(client, register_url, register_user, data, template):
    response = client.post(register_url, data)
    response.user = register_user
    assert response.status_code == 200
    assert template in [template.name for template in response.templates]
