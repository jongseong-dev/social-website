import pytest

from account.factory import ProfileFactory, UserFactory
from account.forms import (
    LoginForm,
    UserRegistrationForm,
    ProfileEditForm,
    UserEditForm,
)


@pytest.fixture(scope="module")
def user_email():
    return "test@test.com"


@pytest.fixture
def user(user_email):
    return UserFactory.create(email=user_email)


@pytest.fixture
def profile(user):
    #
    return ProfileFactory.create()


@pytest.fixture
def user_login_form_data():
    return {"username": "testuser", "password": "testpassword"}


@pytest.fixture
def user_register_form_data():
    return {
        "username": "testuser",
        "first_name": "testname",
        "email": "test@test.com",
        "password": "testpassword",
        "password2": "testpassword",
    }


@pytest.fixture
def user_edit_form_data():
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "update@email.com",
    }


@pytest.mark.django_db
def test_login_form_valid(user_login_form_data):
    form = LoginForm(data=user_login_form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_login_form_empty_username(user_login_form_data):
    user_login_form_data["username"] = ""
    form = LoginForm(data=user_login_form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_login_form_invalid_username(user_login_form_data):
    user_login_form_data["username"] = "a" * 101
    form = LoginForm(data=user_login_form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_user_registration_form_valid(user_register_form_data):
    form = UserRegistrationForm(data=user_register_form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_user_registration_form_empty_username(user_register_form_data):
    user_register_form_data["username"] = ""
    form = UserRegistrationForm(data=user_register_form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_user_registration_form_empty_password(user_register_form_data):
    user_register_form_data["password"] = ""
    form = UserRegistrationForm(data=user_register_form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_user_registration_form_not_match_password(user_register_form_data):
    user_register_form_data["password"] = "testpassword"
    user_register_form_data["password2"] = "wrongpassword"
    form = UserRegistrationForm(data=user_register_form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_user_registration_form_invalid_email(user_register_form_data):
    user_register_form_data["email"] = "invalidemail"
    form = UserRegistrationForm(data=user_register_form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_user_registration_form_email_exists(
    user, user_email, user_register_form_data
):
    user_register_form_data["email"] = user_email
    form = UserRegistrationForm(data=user_register_form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_user_edit_form_clean_email_existing(
    user, user_email, user_edit_form_data
):
    exist_user = UserFactory.create()
    user_edit_form_data["email"] = exist_user.email
    form = UserEditForm(
        instance=user,
        data=user_edit_form_data,
    )
    assert not form.is_valid()


@pytest.mark.django_db
def test_user_edit_form_valid(user, user_edit_form_data):
    form = UserEditForm(
        instance=user,
        data=user_edit_form_data,
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_profile_edit_form_valid_data(transactional_db, user, profile):
    form = ProfileEditForm(
        instance=profile,
        data={"date_of_birth": "2000-01-01", "photo": "test.jpg"},
    )
    assert form.is_valid()


@pytest.mark.django_db
def test_profile_edit_form_invalid_date(profile):
    form = ProfileEditForm(
        instance=profile,
        data={"date_of_birth": "2000-13-01", "photo": "test.jpg"},
    )
    assert not form.is_valid()
