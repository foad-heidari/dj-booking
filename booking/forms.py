from django.db.models import fields
from booking.models import Booking
from django import forms

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields  = ["time", "date", "user_name", "user_email"]
