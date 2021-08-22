Installation
============

dj_booking
------

Python package::

    pip install dj_booking

settings.py ::

    INSTALLED_APPS = [
        ...
        'booking',
        ...
    ]

urls.py::

    urlpatterns = [
        ...
        path('booking/', include('booking.urls')),
        ...
    ]



Post-Installation
-----------------

In your Django root execute the command below to create your database tables::

    python manage.py migrate

Now start your server, and you can visit the pages (e.g. http://localhost:8000/booking/ and http://localhost:8000/booking/admin)
