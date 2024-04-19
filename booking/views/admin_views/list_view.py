

from booking.settings import PAGINATION

from booking.models import Booking
from django.views.generic import ListView
from booking.utils import BookingSettingMixin


class BookingListView(BookingSettingMixin, ListView):
    model = Booking
    template_name = "booking/admin/booking_list.html"
    paginate_by = PAGINATION
