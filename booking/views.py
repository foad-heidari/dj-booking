from booking.models import Booking
from booking.forms import BookingForm
from django.shortcuts import reverse
from django.views.generic import CreateView, TemplateView, ListView


# # # # # # #
# Admin Part
# # # # # # #
class AdminHomeView(TemplateView):
    model = Booking
    template_name = "booking/admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_bookings"] = Booking.objects.filter().order_by(
            "date", "time")[:10]
        context["waiting_bookings"] = Booking.objects.filter(
            approved=False).order_by("-date", "time")[:10]
        return context


class BookingListView(ListView):
    form_class = Booking
    template_name = "booking/admin/appointment_list.html"

    def get_queryset(self):
        return Booking.objects.filter()[:20]
    


# # # # # # # #
# Booking Part
# # # # # # # #
class BookingCreateView(CreateView):
    form_class = BookingForm
    template_name = "booking/user/create_booking.html"

    def get_success_url(self):
        url = reverse("create_booking")
        return url + "?type=successed"
