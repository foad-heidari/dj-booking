 Django Booking
===================

Django Booking is a Complete booking system as a package for Django.


Getting Started
===============
what you get:
   - A booking page which user can book appointment
   - A dashboard which admin can see the appointments and make actions

Requirements
============

Django Booking requires Django 3 or later.


Getting It
==========

<!-- You can get Django Extensions by using pip::

    $ pip install django-extensions -->

If you want to install it from source, grab the git repository from GitHub and run setup.py::

    $ git clone git@github.com:foad-heidari/django-booking.git
    $ cd django-booking
    $ pip install -r requirements.txt


Installing It
=============

To enable `django_booking` in your project you need to add it to `INSTALLED_APPS` in your projects
`settings.py` file::

    INSTALLED_APPS = (
        ...
        'django_booking',
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

- GitHub: https://github.com/foad-heidari/django-booking


Documentation
=============

You can view documentation online at:

- https://django-booking.readthedocs.io

Or you can look at the docs/ directory in the repository.


Support
=======

Django Booking is free and always will be. It is developed and maintained by developers in an Open Source manner.
Any support is welcome. You could help by writing documentation, pull-requests, report issues and/or translations.
