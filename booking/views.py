import datetime

from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, UpdateView

from booking.models import Booking, BookingManager
from booking.forms import BookingCustomerForm, BookingDateForm, BookingTimeForm, BookingManagerForm


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
        return reverse("booking_settings")


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
        context.update({
            'b_manager': BookingManager.objects.first(),
            "progress_width": "6"
        })
        if self.steps.current == 'Time':
            context.update({
                "get_available_time": get_available_time(self.get_cleaned_data_for_step('Date')["date"]),
                "progress_width": "30"
            })
        if self.steps.current == 'User Info':
            context.update({
                "progress_width": "75"
            })
        return context

    def done(self, form_list, **kwargs):
        data = dict((k, v) for form in form_list for k, v in form.cleaned_data.items())
        booking = Booking.objects.create(**data)
        return render(self.request, 'booking/user/booking_done.html', {
            "progress_width": "100",
            "booking_id": booking.id
        })


# class BookingCreateView(CreateView):
#     form_class = BookingForm
#     template_name = "booking/user/create_booking.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         title = settings.BOOKING_TITLE if hasattr(
#             settings, "BOOKING_TITLE") else "Booking"
#         description = settings.BOOKING_DESC if hasattr(
#             settings, "BOOKING_DESC") else "Make your appointment easly with us."
#         context["title"] = title
#         context["description"] = description
#         context["booking_bg"] = settings.BOOKING_BG if hasattr(
#             settings, "BOOKING_BG") else "img/booking_bg.jpg"

#         context["b_manager"] = BookingManager.objects.first()
#         return context

#     def get(self, request, *args, **kwargs):
#         b_manager = BookingManager.objects.first()
#         if not b_manager:
#             b_manager = BookingManager.objects.create(
#                 start_time="09:00", end_time="17:00")
#         if not b_manager.booking_enable:
#             booking_disable_url = settings.BOOKING_DISABLE_URL if hasattr(
#                 settings, "BOOKING_DISABLE_URL") else "/"
#             return redirect(booking_disable_url)
#         return super().get(request, *args, **kwargs)

#     def get_success_url(self):
#         url = settings.BOOKING_SUCCESS_REDIRECT_URL \
#             if hasattr(settings, "BOOKING_SUCCESS_REDIRECT_URL") \
#             else reverse("create_booking") + f"?type=successed&booking_id={self.object.id}"
#         return url

def add_delta(tme, delta):
    # transform to a full datetime first
    return (datetime.datetime.combine(
        datetime.date.today(), tme
    ) + delta).time()

def get_available_time(date):
    b_manager = BookingManager.objects.first()
    existing_bookings = Booking.objects.filter(
        date=date).values_list('time')

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

    return time_list
