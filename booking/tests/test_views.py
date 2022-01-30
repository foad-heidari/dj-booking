from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.encoding import force_str
from booking.models import Booking
from booking.tests.test_forms import DEMO_BOOKING_DATA

DEMO_USER_DATA = {
    "user_name": "booking_user",
    "email": "booking@test.com",
    "password": "booking_password"
}


class TestBookingAdminViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            DEMO_USER_DATA["user_name"], DEMO_USER_DATA["email"], DEMO_USER_DATA["password"],
            is_staff=True,
            is_superuser=True
        )

        self.booking = Booking.objects.create(**DEMO_BOOKING_DATA)

        self.cl = Client()
        # Loggin as stuff user
        self.cl.login(
            username=DEMO_USER_DATA["user_name"], password=DEMO_USER_DATA["password"])

    def test_booking_settings_view(self):

        # booking settings
        response = self.cl.post(
            reverse("booking_settings"),
            {
                "booking_enable": "on",
                "confirmation_required": "on",
                # "disable_weekend": "on",
                "available_booking_months": "1",
                "start_time": "09:00",
                "end_time": "17:00",
                "period_of_each_booking": "30",
            },
        )
        self.assertEqual(response.status_code, 302)

        response = self.cl.get(reverse("booking_settings"))
        self.assertInHTML(
            '<input type="checkbox" name="booking_enable" class=" form-check-input" id="id_booking_enable" checked="">', force_str(response.content))
        self.assertInHTML(
            '<input type="checkbox" name="disable_weekend" class=" form-check-input" id="id_disable_weekend">', force_str(response.content))

    def test_booking_list_view(self):
        # booking List
        response = self.cl.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
            f'<td>{DEMO_BOOKING_DATA["user_name"]}</td>', force_str(response.content))
        self.assertInHTML(
            '<i class="far fa-pause-circle text-danger"></i>', force_str(response.content))

    def test_approve_booking_view(self):
        response = self.cl.get(reverse("booking_update", kwargs={
                               "id": self.booking.id, "type": "approved"}))
        self.assertEqual(response.status_code, 302)
        response = self.cl.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
            '<i class="fas fa-check-square text-success"></i>', force_str(response.content))

    def test_delete_booking_view(self):
        response = self.cl.get(reverse("booking_update", kwargs={
                               "id": self.booking.id, "type": "delete"}))
        self.assertEqual(response.status_code, 302)
        response = self.cl.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
            '<tbody></tbody>', force_str(response.content))



class TestBookingUserViews(TestCase):
    # TODO: Create the test
    pass
