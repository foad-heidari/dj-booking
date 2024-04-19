
from django.shortcuts import  redirect, render
from formtools.wizard.views import SessionWizardView
from booking.models import Booking, BookingSettings
from booking.settings import (BOOKING_BG, BOOKING_DESC, BOOKING_DISABLE_URL,
                              BOOKING_SUCCESS_REDIRECT_URL, BOOKING_TITLE)
from .get_available_times_view import get_available_time

from booking.forms import (BookingCustomerForm, BookingDateForm, BookingTimeForm)
BOOKING_STEP_FORMS = (
    ('Date', BookingDateForm),
    ('Time', BookingTimeForm),
    ('User Info', BookingCustomerForm)
)

class BookingCreateWizardView(SessionWizardView):
    template_name = "booking/user/booking_wizard.html"
    form_list = BOOKING_STEP_FORMS

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        progress_width = "6"
        if self.steps.current == 'Time':
            context["get_available_time"] = get_available_time(
                self.get_cleaned_data_for_step('Date')["date"])
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
            return redirect(BOOKING_DISABLE_URL)

        return self.render_to_response(context)

    def done(self, form_list, **kwargs):
        data = dict((key, value) for form in form_list for key,
                    value in form.cleaned_data.items())
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
