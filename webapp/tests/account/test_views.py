import pytest
from django.test import Client
from django.urls import reverse

from account.factory import UserFactory, ProfileFactory


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
def profile(user):
    return ProfileFactory.create(user=user)


@pytest.fixture
def login(user, plain_password, client):
    client.login(username=user.username, password=plain_password)


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


@pytest.fixture
def edit_url():
    return reverse("edit")


@pytest.mark.django_db
def test_get_dashboard_login_user(
    login, client, user, dashboard_url, plain_password
):
    response = client.get(dashboard_url)
    assert response.status_code == 200
    assert "account/dashboard.html" in [
        template.name for template in response.templates
    ]


@pytest.mark.django_db
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
def test_register(login, client, register_url, data, template):
    response = client.post(register_url, data)
    assert response.status_code == 200
    assert template in [template.name for template in response.templates]


@pytest.mark.django_db
def test_successful_profile_edit(login, profile, client, edit_url):
    success_message = "Profile updated successfully"
    response = client.post(
        edit_url,
        data={"username": "newusername", "email": "newemail@example.com"},
    )
    assert response.status_code == 200
    assert success_message in response.content.decode()

    empty_username_response = client.post(
        edit_url, data={"username": "", "email": "newemail@example.com"}
    )
    assert empty_username_response.status_code == 200
    assert success_message in empty_username_response.content.decode()

    empty_email_response = client.post(
        edit_url, data={"username": "newusername2", "email": ""}
    )
    assert empty_email_response.status_code == 200
    assert success_message in empty_email_response.content.decode()


@pytest.mark.django_db
def test_edit_profile_without_login(profile, client, edit_url):
    response = client.post(
        edit_url,
        data={"username": "newusername", "email": "newemail@example.com"},
    )
    assert "login" in response.url
