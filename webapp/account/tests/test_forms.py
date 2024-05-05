from django.test import TestCase

from webapp.account.forms import LoginForm


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
