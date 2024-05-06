from urllib.parse import quote_plus

from django.test import TestCase, Client
from django.urls import reverse

from ..factory import UserFactory


class DashboardViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.plain_password = "password"
        cls.user = UserFactory.create(password=cls.plain_password)
        cls.url = reverse("dashboard")

    def test_get_dashboard_login_user_200_OK(self):
        self.client.login(
            username=self.user.username,
            password=self.plain_password,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/dashboard.html")

    def test_dashboard_unauthenticated_user_redirect_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        expected_url = reverse("login") + "?next=" + quote_plus(self.url)
        self.assertRedirects(response, expected_url)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("register")
        self.user = UserFactory.create(
            username="testuser", email="test@test.com", password="testpassword"
        )

    def test_form_is_valid_with_correct_data(self):
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "newpassword",
                "password2": "newpassword",
            },
        )
        response.user = self.user
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/register_done.html")

    def test_form_is_invalid_with_empty_username(self):
        response = self.client.post(
            self.url,
            {
                "username": "",
                "email": "newuser@test.com",
                "password": "newpassword",
                "password2": "newpassword",
            },
        )
        response.user = self.user
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/register.html")

    def test_form_is_invalid_with_empty_password(self):
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "",
                "password2": "newpassword",
            },
        )
        response.user = self.user
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/register.html")

    def test_form_is_invalid_with_mismatched_passwords(self):
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "email": "newuser@test.com",
                "password": "newpassword",
                "password2": "wrongpassword",
            },
        )
        response.user = self.user
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/register.html")

    def test_form_is_invalid_with_invalid_email(self):
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "email": "invalidemail",
                "password": "newpassword",
                "password2": "newpassword",
            },
        )
        response.user = self.user
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/register.html")
