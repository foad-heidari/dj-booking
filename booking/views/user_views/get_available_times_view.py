import datetime
from typing import Dict, List

from booking.models import Booking, BookingSettings



def add_delta(time: datetime.time, delta: datetime.timedelta) -> datetime.time:
    """
    Adds a time delta to a datetime.time object and returns the updated time.

    Args:
        time (datetime.time): The initial time.
        delta (datetime.timedelta): The time delta to add.

    Returns:
        datetime.time: The updated time after adding the delta.
    """
    # Combine the input time with today's date, add the delta, and return the updated time.
    return (datetime.datetime.combine(datetime.date.today(), time) + delta).time()

def get_available_time(date: datetime.date) -> list:
    """
    Generates a list of available time slots for a specific date, based on booking settings.

    Each time slot is represented as a dictionary containing the time and its availability.
    The times are checked between start_time and end_time defined in booking settings.
    If a time slot has reached its booking capacity, it is marked as 'is_taken'.

    Args:
        date (datetime.date): The date for which to check available time slots.

    Returns:
        list: A list of dictionaries, each containing the 'time' (as a string) and 'is_taken' (as a boolean).
    """
    # Retrieve the booking settings; if none are available, return an empty list
    settings = BookingSettings.objects.first()
    if not settings:
        return []

    time_slots = []
    start_time = settings.start_time
    end_time = settings.end_time
    # Retrieve a list of all times booked for the given date to determine availability
    booked_times = list(Booking.objects.filter(date=date).values_list('time', flat=True))

    # Iterate over each time slot from start_time to end_time
    while start_time <= end_time:
        # Determine if the time slot is fully booked
        is_taken = booked_times.count(start_time) >= settings.max_booking_per_time

        # Append the time and its availability to the list of time slots
        time_slots.append({
            "time": start_time.strftime("%H:%M"),
            "is_taken": is_taken
        })

        # Increment the time by the booking period interval
        start_time = add_delta(start_time, datetime.timedelta(minutes=int(settings.period_of_each_booking)))

    return time_slots