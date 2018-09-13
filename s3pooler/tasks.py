from celery.decorators import periodic_task
from .vilma.s3scrapper import S3Scrapper
from .vilma.raw_vision import RawVision
from datetime import timedelta
from .models import Datetimes
from .visions import UsersVision
from django.db import transaction

@periodic_task(run_every=timedelta(seconds=15))
def scrapp_s3(files_to_scrap=10):
    scrapper = S3Scrapper()
    timestamp_before = Datetimes.objects.last_timestamp('s3pooler')
    nr_registered = scrapper.scrapp_save_update_datetime(timestamp_before, files_to_scrap)
    timestamp_after = Datetimes.objects.last_timestamp('s3pooler')
    message = '''Task Done : {} events scrapped,      timestamp
    # before: {} , after : {}'''.format(nr_registered, timestamp_before, timestamp_after)
    print(message)
    update_visions.delay(timestamp_before, timestamp_after)
    return nr_registered

@periodic_task(run_every=timedelta(seconds=10),
               queue='users',
               options={'queue': 'users'})
def update_visions(timestamp_before=None, timestamp_after=None):
    raw = RawVision()
    users = UsersVision()
    if timestamp_after==None:
        timestamp_before = Datetimes.objects.last_timestamp('visions')
    with transaction.atomic():
        raw_saved = raw.pool_save_update_tables(timestamp_before, timestamp_after)
        users_saved = users.pool_save(timestamp_before, timestamp_after)
    message = '''Task Done : Visions Updated, ({}, {})     timestamp
    before: {} , after : {}'''.format(raw_saved, users_saved, timestamp_before, timestamp_after)
    print(message)
    return (raw_saved, users_saved)
