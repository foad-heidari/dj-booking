from django.urls import path

from .views import BookingCreateView, AdminHomeView, BookingListView, BookingSettingsView


urlpatterns = [
        path("booking/", BookingCreateView.as_view(), name="create_booking"),
        path("booking/admin", AdminHomeView.as_view(), name="admin_dashboard"),
        path("booking/admin/list", BookingListView.as_view(), name="booking_list"),
        path("booking/admin/settings", BookingSettingsView.as_view(), name="booking_settings"),
]