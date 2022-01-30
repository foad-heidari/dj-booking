from booking.models import Booking, BookingSettings
from django.contrib import admin


admin.site.register(Booking)
# TODO: remove BookingSettings
admin.site.register(BookingSettings)

