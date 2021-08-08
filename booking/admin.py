from booking.models import Booking, BookingManager
from django.contrib import admin


admin.site.register(Booking)
# TODO: remove BookingManager
admin.site.register(BookingManager)

