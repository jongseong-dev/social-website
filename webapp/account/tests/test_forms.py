from django.test import TestCase

from ..forms import LoginForm
from ..forms import UserRegistrationForm


class LoginFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {"username": "testuser", "password": "testpassword"}

    def test_form_is_valid_with_correct_data(self):
        form = LoginForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_with_empty_username(self):
        self.form_data["username"] = ""
        form = LoginForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_with_empty_password(self):
        self.form_data["password"] = ""
        form = LoginForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_with_long_username(self):
        self.form_data["username"] = "a" * 101
        form = LoginForm(data=self.form_data)
        self.assertFalse(form.is_valid())


class UserRegistrationFormTest(TestCase):
    def setUp(self):
        self.form_data = {
            "username": "testuser",
            "first_name": "testname",
            "email": "test@test.com",
            "password": "testpassword",
            "password2": "testpassword",
        }

    def test_form_is_valid_with_correct_data(self):
        form = UserRegistrationForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_with_empty_username(self):
        self.form_data["username"] = ""
        form = UserRegistrationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_with_empty_password(self):
        self.form_data["password"] = ""
        form = UserRegistrationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_with_mismatched_passwords(self):
        self.form_data["password"] = "testpassword"
        self.form_data["password2"] = "wrongpassword"
        form = UserRegistrationForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def form_is_invalid_with_invalid_email(self):
        self.form_data["email"] = "invalidemail"
        form = UserRegistrationForm(data=self.form_data)
        self.assertFalse(form.is_valid())
