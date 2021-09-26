import datetime
import json

from django.contrib import messages
from django.shortcuts import reverse, redirect, get_object_or_404
from django.http.response import HttpResponse
from django.conf import settings
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
            return BookingManager.objects.create(start_time="09:00", end_time="17:00")

    def get_success_url(self):
        return reverse("booking_settings") + "?type=successed"


def bookingUpdateView(request, id, type):
    if request.method == "GET":
        item = get_object_or_404(Booking, id=id)
        if type == "delete":
            item.delete()
            messages.warning(request, "The item successfully deleted!")
        elif type == "approved":
            item.approved = True
            item.save()
            messages.success(request, "The item successfully approved!")

        return redirect(reverse("booking_list"))

    return redirect(reverse("create_booking"))


# # # # # # # #
# Booking Part
# # # # # # # #

def add_delta(tme, delta):
    # transform to a full datetime first
    return (datetime.datetime.combine(
        datetime.date.today(), tme
    ) + delta).time()


class BookingCreateView(CreateView):
    form_class = BookingForm
    template_name = "booking/user/create_booking.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = settings.BOOKING_TITLE if hasattr(settings,"BOOKING_TITLE") else "Booking"
        description = settings.BOOKING_DESC if hasattr(settings,"BOOKING_DESC") else "Make your appointment easly with us."
        context["title"] = title
        context["description"] = description

        return context

    def get_success_url(self):
        url = reverse("create_booking")
        return url + f"?type=successed&booking_id={self.object.id}"


def get_available_time(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))

        b_manager = BookingManager.objects.first()
        if not b_manager:
            b_manager = BookingManager.objects.create(start_time="09:00", end_time="17:00")
        existing_bookings = Booking.objects.filter(
            date=post_data["date"]).values_list('time')
        next_time = b_manager.start_time
        time_list = []
        while True:
            is_taken = any([x[0] == next_time for x in existing_bookings])
            time_list.append(
                {"time": ":".join(str(next_time).split(":")[:-1]), "is_taken": is_taken})
            next_time = add_delta(next_time, datetime.timedelta(
                minutes=int(b_manager.period_of_each_booking)))
            if next_time > b_manager.end_time:
                break
        data = json.dumps({'time_list': time_list})
        return HttpResponse(data, content_type='application/json')
