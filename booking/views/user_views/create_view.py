
from django.shortcuts import  redirect, render
from formtools.wizard.views import SessionWizardView
from booking.models import Booking, BookingSettings
from booking.settings import (BOOKING_BG, BOOKING_DESC, BOOKING_DISABLE_URL,
                              BOOKING_SUCCESS_REDIRECT_URL, BOOKING_TITLE)
from .get_available_times_view import get_available_time
from booking.forms import (BookingCustomerForm, BookingDateForm, BookingTimeForm)

# Mapping of form steps in the booking process.
BOOKING_STEP_FORMS = (
    ('Date', BookingDateForm),
    ('Time', BookingTimeForm),
    ('User Info', BookingCustomerForm)
)


class BookingCreateWizardView(SessionWizardView):
    """A wizard view for creating new bookings, managing multi-step form submissions."""
    
    template_name = "booking/user/booking_wizard.html"
    form_list = BOOKING_STEP_FORMS

    def get_context_data(self, form, **kwargs):
        """
        Extends the context for the template with additional booking-related data.
        
        Args:
            form: The current form instance being processed.
        
        Returns:
            A dictionary containing context data for the template.
        """
        # Initialize context data from the base class
        context = super().get_context_data(form=form, **kwargs)
        progress_widths = {'Date': '6', 'Time': '30', 'User Info': '75'}
        current_step = self.steps.current

        # Update the context with dynamic values based on the current step in the wizard
        context.update({
            'progress_width': progress_widths.get(current_step, '0'),
            'booking_settings': self.get_booking_settings(),
            'booking_bg': BOOKING_BG,
            'description': BOOKING_DESC,
            'title': BOOKING_TITLE,
        })
        
        # Add available times to the context when at the 'Time' step
        if current_step == 'Time':
            context['get_available_time'] = get_available_time(
                self.get_cleaned_data_for_step('Date')['date'])

        return context

    def get_booking_settings(self):
        """Caches and returns the first BookingSettings instance to minimize database queries."""
        if not hasattr(self, '_booking_settings'):
            self._booking_settings = BookingSettings.objects.first()
        return self._booking_settings

    def render(self, form=None, **kwargs):
        """
        Custom render method to handle the response based on booking settings.
        
        Args:
            form: The form instance to render, if not provided, uses the current form.
        
        Returns:
            HttpResponse object either rendering the form or redirecting if booking is disabled.
        """
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)

        # Redirect if booking is disabled in the settings
        if not context['booking_settings'].booking_enable:
            return redirect(BOOKING_DISABLE_URL)

        return self.render_to_response(context)

    def done(self, form_list, **kwargs):
        """
        Processes the forms when all steps are completed.
        
        Args:
            form_list: A list of form instances from each step.
        
        Returns:
            Redirect to a success URL or render a completion template.
        """
        # Consolidate form data into a single dictionary and create a booking instance
        data = {key: value for form in form_list for key, value in form.cleaned_data.items()}
        booking = Booking.objects.create(**data)
        
        # Redirect to success URL if specified, otherwise render a completion template
        if BOOKING_SUCCESS_REDIRECT_URL:
            return redirect(BOOKING_SUCCESS_REDIRECT_URL)
        
        return render(
            self.request, 'booking/user/booking_done.html', {
                "progress_width": "100",
                "booking_id": booking.id,
                "booking_bg": BOOKING_BG,
                "description": BOOKING_DESC,
                "title": BOOKING_TITLE,
            })