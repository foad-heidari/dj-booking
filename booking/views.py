from django.shortcuts import reverse
# from django.contrib.auth.decorators import user_passes_test
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, ListView, UpdateView

from booking.models import Booking, BookingManager
from booking.forms import BookingForm, BookingManagerForm

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


# @method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class BookingSettingsView(UpdateView):
    form_class = BookingManagerForm
    template_name = "booking/admin/appointment_settings.html"
    
    def get_object(self):
        obj = BookingManager.objects.filter()
        if obj.exists():
            return obj[0]
        else:
            return BookingManager.objects.create(start_time="09:00",end_time="17:00")
    
    def get_success_url(self):
        return reverse("booking_settings") + "?type=successed"


# # # # # # # #
# Booking Part
# # # # # # # #
class BookingCreateView(CreateView):
    form_class = BookingForm
    template_name = "booking/user/create_booking.html"

    def get_success_url(self):
        url = reverse("create_booking")
        return url + "?type=successed"
