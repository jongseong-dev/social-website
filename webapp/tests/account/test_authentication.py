import pytest

from account.factory import UserFactory
from account.authentication import EmailAuthBackend


@pytest.fixture
def plain_password():
    return "testpassword"


@pytest.fixture
def user(plain_password):
    return UserFactory.create(password=plain_password)


@pytest.fixture
def auth_backend():
    return EmailAuthBackend()


@pytest.mark.django_db
def test_authenticate_with_correct_credentials(
    user, plain_password, auth_backend
):
    assert auth_backend.authenticate(None, user.email, plain_password) == user


@pytest.mark.django_db
def test_authenticate_with_incorrect_password(user, auth_backend):
    assert auth_backend.authenticate(None, user.email, "wrongpassword") is None


@pytest.mark.django_db
def test_authenticate_with_nonexistent_email(plain_password, auth_backend):
    assert (
        auth_backend.authenticate(
            None, "nonexistent@example.com", plain_password
        )
        is None
    )


@pytest.mark.django_db
def test_get_user_with_existing_id(user, auth_backend):
    assert auth_backend.get_user(user.id) == user


@pytest.mark.django_db
def test_get_user_with_nonexistent_id(auth_backend):
    assert auth_backend.get_user(9999) is None
