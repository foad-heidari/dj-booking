from django.urls import path

from .views import (BookingApproveView, BookingCreateWizardView,
                    BookingDeleteView, BookingHomeView, BookingListView,
                    BookingSettingsView, get_available_time)

urlpatterns = [
    path("", BookingCreateWizardView.as_view(), name="create_booking"),
    path("admin", BookingHomeView.as_view(), name="admin_dashboard"),
    path("admin/list", BookingListView.as_view(), name="booking_list"),
    path("admin/settings", BookingSettingsView.as_view(), name="booking_settings"),
    path("admin/<pk>/delete",
         BookingDeleteView.as_view(), name="booking_delete"),
    path("admin/<pk>/approve",
         BookingApproveView.as_view(), name="booking_approve"),
    path("get-available-time", get_available_time, name="get_available_time"),
]
