from django.contrib import admin

from booking.models import Booking, BookingSettings

admin.site.register(Booking)
# TODO: remove BookingSettings
admin.site.register(BookingSettings)

