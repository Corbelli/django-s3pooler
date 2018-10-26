# Django-S3Poller


Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "s3pooler" to your INSTALLED_APPS BEFORE YOUR APPS setting like this::

    INSTALLED_APPS = [
        ...
        's3pooler',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('s3pooler/', include('polls.urls')),

3. Run `python manage.py migrate` to create the models.

