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
