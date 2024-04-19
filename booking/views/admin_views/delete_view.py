
from booking.models import Booking
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from booking.utils import BookingSettingMixin
                                

class BookingDeleteView(BookingSettingMixin, DeleteView):
    mdoel = Booking
    success_url = reverse_lazy('booking_list')
    queryset = Booking.objects.filter()


