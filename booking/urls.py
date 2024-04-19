from django.urls import path

# USer
from .views.user_views.create_view import BookingCreateWizardView
from .views.user_views.get_available_times_view import get_available_time

# ADMIN
from .views.admin_views.home_view import BookingHomeView
from .views.admin_views.list_view import BookingListView
from .views.admin_views.settings_view import BookingSettingsView
from .views.admin_views.delete_view import BookingDeleteView
from .views.admin_views.approve_view import BookingApproveView

urlpatterns = [
    path("", BookingCreateWizardView.as_view(), name="create_booking"),
    path("get-available-time", get_available_time, name="get_available_time"),

     # Admin Views
    path("admin", BookingHomeView.as_view(), name="admin_dashboard"),
    path("admin/list", BookingListView.as_view(), name="booking_list"),
    path("admin/settings", BookingSettingsView.as_view(), name="booking_settings"),
    path("admin/<pk>/delete",
         BookingDeleteView.as_view(), name="booking_delete"),
    path("admin/<pk>/approve",
         BookingApproveView.as_view(), name="booking_approve"),
]
