from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

DEMO_DATA = {
    "user_name": "booking_user",
    "email": "booking@test.com",
    "password": "booking_password"
}


class TestPermissions(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            DEMO_DATA["user_name"], DEMO_DATA["email"], DEMO_DATA["password"], is_staff=True)

    def test_admin_view_permissions(self):
        # admin_dashboard
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 302)
        # booking_list
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 302)
        # booking_settings
        response = self.client.get(reverse("booking_settings"))
        self.assertEqual(response.status_code, 302)

        # Loggin as stuff user
        self.client.login(
            username=DEMO_DATA["user_name"], password=DEMO_DATA["password"])

        # admin_dashboard
        response = self.client.get(reverse("admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        # booking_list
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)
        # booking_settings
        response = self.client.get(reverse("booking_settings"))
        self.assertEqual(response.status_code, 200)
