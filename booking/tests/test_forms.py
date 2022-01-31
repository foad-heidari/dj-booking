import datetime

from django.test import TestCase

from booking.forms import (BookingCustomerForm, BookingDateForm,
                           BookingSettingsForm, BookingTimeForm)

DEMO_BOOKING_DATA = {
        "date": (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        "time": "12:00",
        "user_name": "test_user",
        "user_email": "user@email.com",
        "user_mobile": ""
    }

class TestBookingCreateForms(TestCase):
    data = DEMO_BOOKING_DATA

    def test_date_form(self):
        # Test the valid form
        form = BookingDateForm(data=self.data)
        validated = form.is_valid()
        self.assertTrue(validated)

        # Test the validation
        self.data["date"] = "08:00"
        form = BookingDateForm(data=self.data)
        validated = form.is_valid()
        self.assertFalse(validated)
        self.assertEqual(form.errors["date"][0], "Enter a valid date.")

        # Test for requreid fields error
        del self.data["date"]
        form = BookingDateForm(data=self.data)
        validated = form.is_valid()
        self.assertFalse(validated)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(len(form.errors["date"]), 1)
        self.assertEqual(form.errors["date"][0], "This field is required.")

    def test_time_form(self):
        # Test the valid form
        form = BookingTimeForm(data=self.data)
        validated = form.is_valid()
        self.assertTrue(validated)

        # Test the validation
        self.data["time"] = "asd"
        form = BookingTimeForm(data=self.data)
        validated = form.is_valid()
        self.assertFalse(validated)
        self.assertEqual(form.errors["time"][0], "Enter a valid time.")

        # Test for requreid fields error
        del self.data["time"]
        form = BookingTimeForm(data=self.data)
        validated = form.is_valid()
        self.assertFalse(validated)
        self.assertEqual(len(form.errors), 1)
        self.assertEqual(len(form.errors["time"]), 1)

    def test_customer_form(self):
        # Test the valid form
        form = BookingCustomerForm(data=self.data)
        validated = form.is_valid()
        self.assertTrue(validated)

        # Test the validation
        self.data["user_email"] = "asd"
        form = BookingCustomerForm(data=self.data)
        validated = form.is_valid()
        self.assertFalse(validated)
        self.assertEqual(form.errors["user_email"]
                         [0], "Enter a valid email address.")

        # Test for requreid fields error
        del self.data["user_name"]
        del self.data["user_email"]

        form = BookingCustomerForm(data=self.data)
        validated = form.is_valid()
        self.assertFalse(validated)
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(form.errors["user_name"]
                         [0], "This field is required.")
        self.assertEqual(form.errors["user_email"]
                         [0], "This field is required.")


# Test the Booking Setting Form
class TestBookingSettingsForm(TestCase):
    def test_settings_form(self):
        data = {
            "start_time": "09:00",
            "end_time": "17:00",
            "booking_enable": True,
            "confirmation_required": True,
            "available_booking_months": 1,
            "max_booking_per_time": 1,
            "period_of_each_booking": "30",
        }

        # Test the valid form
        form = BookingSettingsForm(data=data)
        validated = form.is_valid()
        self.assertTrue(validated)

        # Test the validation
        data["end_time"] = "08:00"
        form = BookingSettingsForm(data=data)
        validated = form.is_valid()
        self.assertFalse(validated)
        self.assertEqual(len(form.non_field_errors()), 1)
        self.assertEqual(
            form.non_field_errors()[
                0], "The end time must be later than start time."
        )

        # Test for requreid fields error
        del data["start_time"]
        del data["end_time"]
        form = BookingSettingsForm(data=data)
        validated = form.is_valid()
        self.assertFalse(validated)
        self.assertEqual(len(form.non_field_errors()), 0)
        self.assertEqual(len(form.errors), 2)
        self.assertEqual(len(form.errors["end_time"]), 1)
        self.assertEqual(form.errors["end_time"][0], "This field is required.")
        self.assertEqual(len(form.errors["start_time"]), 1)
        self.assertEqual(form.errors["start_time"]
                         [0], "This field is required.")
