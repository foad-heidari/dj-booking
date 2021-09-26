import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name = 'dj-booking',
    version = '1.5',
    description = 'Django Booking is a complete Django booking system as a package.',
    long_description=README,
    long_description_content_type='text/markdown',
    url = 'https://github.com/foad-heidari/dj-booking',
    author = 'Foad',
    author_email = 'foad.haydri.1377@gmail.com',
    license = 'MIT',
    maintainer = 'Foad',
    maintainer_email = 'foad.haydri.1377@gmail.com',
    keywords = 'django booking appointment appointment-booking booking-system appointment-system doctor-appointment-booking',
    packages=find_packages(),
    include_package_data=True,

    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)


