import pytest
from account.forms import LoginForm, UserRegistrationForm


@pytest.mark.django_db
def test_login_form():
    form_data = {"username": "testuser", "password": "testpassword"}
    form = LoginForm(data=form_data)
    assert form.is_valid()

    form_data["username"] = ""
    form = LoginForm(data=form_data)
    assert not form.is_valid()

    form_data["username"] = "a" * 101
    form = LoginForm(data=form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_user_registration_form():
    form_data = {
        "username": "testuser",
        "first_name": "testname",
        "email": "test@test.com",
        "password": "testpassword",
        "password2": "testpassword",
    }
    form = UserRegistrationForm(data=form_data)
    assert form.is_valid()

    form_data["username"] = ""
    form = UserRegistrationForm(data=form_data)
    assert not form.is_valid()

    form_data["password"] = ""
    form = UserRegistrationForm(data=form_data)
    assert not form.is_valid()

    form_data["password"] = "testpassword"
    form_data["password2"] = "wrongpassword"
    form = UserRegistrationForm(data=form_data)
    assert not form.is_valid()

    form_data["email"] = "invalidemail"
    form = UserRegistrationForm(data=form_data)
    assert not form.is_valid()
