Configuration
=============

**Available settings:**

``BOOKING_TITLE:``
    Title of create booking page

``BOOKING_DESC``
    Description of create booking page

``BOOKING_BG``
    Background image for create booking page

``BOOKING_SUCCESS_REDIRECT_URL``
    Success redirect url for create booking page

``BOOKING_DISABLE_URL``
    Redirect to this url if create booking is disable

-----

**Usage:**

Add this vars to settings.py

  .. code-block:: python

    BOOKING_TITLE = "Your title"
    BOOKING_DESC = "Your description"
    BOOKING_BG = "img/booking_bg.jpg"

    BOOKING_SUCCESS_REDIRECT_URL = "Success redirect url"
    BOOKING_DISABLE_URL = "Redirect to this url if create booking is disable"
