 Django Booking
===============

Django Booking is a Complete Django booking system.


Overview
===============
what you get:
   - A booking page which user can book appointment.
   - A dashboard which admin can see the appointments and make actions

Requirements
============

Django Booking requires Django 3 or later.


Getting It
==========

    $ pip install dj-booking

Installing it
=============

To enable `dj_booking` in your project you need to add it to `INSTALLED_APPS` in your projects
`settings.py` file::

    INSTALLED_APPS = (
        ...
        'dj_booking',
        ...
    )


And include dj_booking to yor urls::

    urlpatterns = (
        ...
        path("booking/", include("booking.urls")),
        ...
    )


Using It
========

    $ python manage.py migrate
    $ python mange.py runserver

then you can visit the pages::

- booking page: http://localhost:8000/booking
- booking page: http://localhost:8000/booking/admin


Getting Involved
================

Open Source projects can always use more help. Fixing a problem, documenting a feature, adding
translation in your language. If you have some time to spare and like to help us, here are the places to do so:

- GitHub: https://github.com/foad-heidari/dj-booking


Documentation
=============

You can view documentation online at:

- https://dj-booking.readthedocs.io

Or you can look at the docs/ directory in the repository.


Support
=======

Django Booking is free and always will be. It is developed and maintained by developers in an Open Source manner.
Any support is welcome. You could help by writing documentation, pull-requests, report issues and/or translations.
