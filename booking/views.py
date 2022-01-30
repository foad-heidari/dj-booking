import datetime
from typing import Dict, List

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, TemplateView, UpdateView
from formtools.wizard.views import SessionWizardView

from booking.forms import (BookingCustomerForm, BookingDateForm,
                           BookingSettingsForm, BookingTimeForm)
from booking.models import Booking, BookingSettings
from booking.settings import (BOOKING_BG, BOOKING_DESC, BOOKING_DISABLE_URL,
                              BOOKING_SUCCESS_REDIRECT_URL, BOOKING_TITLE,
                              PAGINATION)
from booking.utils import BookingSettingMixin


# # # # # # #
# Admin Part
# # # # # # #
class AdminHomeView(BookingSettingMixin, TemplateView):
    model = Booking
    template_name = "booking/admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_bookings"] = Booking.objects.filter().order_by(
            "date", "time")[:10]
        context["waiting_bookings"] = Booking.objects.filter(
            approved=False).order_by("-date", "time")[:10]
        return context


class BookingListView(BookingSettingMixin, ListView):
    model = Booking
    template_name = "booking/admin/appointment_list.html"
    paginate_by = PAGINATION


class BookingSettingsView(BookingSettingMixin, UpdateView):
    form_class = BookingSettingsForm
    template_name = "booking/admin/appointment_settings.html"

    def get_object(self):
        return BookingSettings.objects.filter().first()

    def get_success_url(self):
        return reverse("booking_settings")


@require_http_methods(["GET", "POST"])
@staff_member_required
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
named_contact_forms = (
    ('Date', BookingDateForm),
    ('Time', BookingTimeForm),
    ('User Info', BookingCustomerForm)
)


class BookingCreateWizardView(SessionWizardView):
    template_name = "booking/user/booking_wizard.html"
    form_list = named_contact_forms

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        progress_width = "6"
        if self.steps.current == 'Time':
            context.update({
                "get_available_time": get_available_time(self.get_cleaned_data_for_step('Date')["date"]),
            })
            progress_width = "30"
        if self.steps.current == 'User Info':
            progress_width = "75"

        context.update({
            'booking_settings': BookingSettings.objects.first(),
            "progress_width": progress_width,
            "booking_bg": BOOKING_BG,
            "description": BOOKING_DESC,
            "title": BOOKING_TITLE

        })
        return context

    def render(self, form=None, **kwargs):
        # Check if Booking is Disable
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)

        if not context["booking_settings"].booking_enable:
            return redirect(BOOKING_DISABLE_URL if BOOKING_DISABLE_URL else "/")

        return self.render_to_response(context)

    def done(self, form_list, **kwargs):
        data = dict((k, v) for form in form_list for k,
                    v in form.cleaned_data.items())
        booking = Booking.objects.create(**data)

        if BOOKING_SUCCESS_REDIRECT_URL:
            return redirect(BOOKING_SUCCESS_REDIRECT_URL)

        return render(self.request, 'booking/user/booking_done.html', {
            "progress_width": "100",
            "booking_id": booking.id,
            "booking_bg": BOOKING_BG,
            "description": BOOKING_DESC,
            "title": BOOKING_TITLE
        })


def add_delta(time: datetime.time, delta: datetime.datetime) -> datetime.time:
    # transform to a full datetime first
    return (datetime.datetime.combine(
        datetime.date.today(), time
    ) + delta).time()


def get_available_time(date: datetime.date) -> List[Dict[datetime.time, bool]]:
    """
    Check for all available time for selected date
    The times should ne betwwen start_time and end_time
    If the time already is taken -> is_taken = True
    """
    booking_settings = BookingSettings.objects.first()
    existing_bookings = Booking.objects.filter(
        date=date).values_list('time')

    next_time = booking_settings.start_time
    time_list = []
    while True:
        is_taken = any([x[0] == next_time for x in existing_bookings])
        time_list.append(
            {"time": ":".join(str(next_time).split(":")[:-1]), "is_taken": is_taken})
        next_time = add_delta(next_time, datetime.timedelta(
            minutes=int(booking_settings.period_of_each_booking)))
        if next_time > booking_settings.end_time:
            break

    return time_list
