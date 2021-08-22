from django.urls import path

from .views import BookingCreateView, AdminHomeView, BookingListView, BookingSettingsView, bookingUpdateView, get_available_time


urlpatterns = [
        path("", BookingCreateView.as_view(), name="create_booking"),
        path("admin", AdminHomeView.as_view(), name="admin_dashboard"),
        path("admin/list", BookingListView.as_view(), name="booking_list"),
        path("admin/settings", BookingSettingsView.as_view(), name="booking_settings"),
        path("<int:id>/<str:type>", bookingUpdateView, name="booking_update"),
        path("get-available-time", get_available_time, name="get_available_time"),
]