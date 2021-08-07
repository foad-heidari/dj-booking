from django.db import models
from django.conf import settings


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField()
    time = models.TimeField()
    user_name = models.CharField(max_length=250)
    user_email = models.EmailField()
    approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return self.user_name or "(No Name)"


# class BookingManager(models.Model):
    pass
    # Enable Booking : Default true
    # Booking type : Default Day and time
    # required Confirmation? : Default Yes
    # Login Required: Default False

    # # Date
    # dissable weekend : Default True
    # start work day : Default Moday
    # max next bokking month : default 1
    # Max Appointment per Day : can be None

    # # time
    # Sart Time : Default 09:00
    # End Time : Default 17:00
    # period of each appointment : Default 30 min
    # max appointmnet per eacth time : Default 1

    # # Other
    # Name
    # Email
    # Address
    # Phone number
    # description
