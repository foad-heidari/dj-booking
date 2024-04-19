import datetime
from typing import Dict, List

from booking.models import Booking, BookingSettings


def add_delta(time: datetime.time, delta: datetime.datetime) -> datetime.time:
    # transform to a full datetime first
    return (datetime.datetime.combine(
        datetime.date.today(), time
    ) + delta).time()


def get_available_time(date: datetime.date) -> list:
    """
    Check for all available time for selected date
    The times should ne betwwen start_time and end_time
    If the time already is taken -> is_taken = True
    """
    settings = BookingSettings.objects.first()
    if not settings:
        return []

    time_slots = []
    start_time = settings.start_time
    end_time = settings.end_time
    booked_times = list(Booking.objects.filter(date=date).values_list('time', flat=True))

    while start_time <= end_time:
        is_taken = booked_times.count(start_time) >= settings.max_booking_per_time
        time_slots.append({
            "time": start_time.strftime("%H:%M"),
            "is_taken": is_taken
        })
        start_time = add_delta(start_time, datetime.timedelta(
            minutes=int(settings.period_of_each_booking)))
    return time_slots
