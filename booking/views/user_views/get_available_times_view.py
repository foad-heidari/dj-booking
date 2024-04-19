import datetime
from typing import Dict, List

from booking.models import Booking, BookingSettings


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
    existing_bookings = [x[0] for x in existing_bookings]
    next_time = booking_settings.start_time
    time_list = []
    while next_time <= booking_settings.end_time:
        is_taken = False
        for x in existing_bookings:
            if x == next_time and \
                existing_bookings.count(x) >= booking_settings.max_booking_per_time:
                is_taken = True

        time_list.append(
            {"time": ":".join(str(next_time).split(":")[:-1]), "is_taken": is_taken})

        next_time = add_delta(next_time, datetime.timedelta(
            minutes=int(booking_settings.period_of_each_booking)))



    return time_list
