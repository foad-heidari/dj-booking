
from booking.models import Booking
from django.urls import reverse_lazy
from django.views.generic import View
from booking.utils import BookingSettingMixin
from django.shortcuts import get_object_or_404, redirect           

class BookingApproveView(BookingSettingMixin, View):
    mdoel = Booking
    success_url = reverse_lazy('booking_list')
    fields = ("approved",)

    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=self.kwargs.get("pk"))
        booking.approved = True
        booking.save()

        return redirect(self.success_url)

