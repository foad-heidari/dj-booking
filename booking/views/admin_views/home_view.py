from booking.settings import PAGINATION

from booking.models import Booking
from django.views.generic import TemplateView
from booking.utils import BookingSettingMixin


class BookingHomeView(BookingSettingMixin, TemplateView):
    model = Booking
    template_name = "booking/admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_bookings"] = Booking.objects.filter().order_by(
            "date", "time")[:10]
        context["waiting_bookings"] = Booking.objects.filter(
            approved=False).order_by("-date", "time")[:10]
        return context
