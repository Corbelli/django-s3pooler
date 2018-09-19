from celery.decorators import periodic_task
from .vilma.s3scrapper import S3Scrapper
from .vilma.raw_vision import RawVision
from datetime import timedelta
from .models import Datetimes
from .visions import UsersVision
from django.db import transaction
from celery import shared_task


@periodic_task(run_every=timedelta(seconds=20))
def scrapp_s3(files_to_scrap=5):
    scrapper = S3Scrapper()
    timestamp_before = Datetimes.objects.last_timestamp('s3pooler')
    nr_registered = scrapper.scrapp_save_update_datetime(timestamp_before, files_to_scrap)
    timestamp_after = Datetimes.objects.last_timestamp('s3pooler')
    message = '''Task Done : {} events scrapped,      timestamp
    # before: {} , after : {}'''.format(nr_registered, timestamp_before, timestamp_after)
    print(message)
    transaction.on_commit(lambda: update_raw.delay(timestamp_before, timestamp_after))
    return nr_registered

@periodic_task(run_every=timedelta(seconds=10))#,
               #queue='users',
               #options={'queue': 'users'})
def update_raw(timestamp_before=None, timestamp_after=None):
    raw = RawVision()
    if timestamp_after==None:
        timestamp_before = Datetimes.objects.last_timestamp('raw_vision')
    raw_saved = raw.pool_save_update_tables(timestamp_before, timestamp_after)
    message = '''Raw Updated, {} timestamp before: {} , after : {}'''.\
        format(raw_saved, timestamp_before, timestamp_after)
    print(message)
    transaction.on_commit(lambda: update_users.delay(timestamp_before, timestamp_after))
    return raw_saved

@shared_task()#queue='users')
def update_users(timestamp_before=None, timestamp_after=None):
    users = UsersVision()
    users_saved = users.pool_save(timestamp_before, timestamp_after)
    message = '''Users Updated, {}  timestamp before: {} , after : {}'''.\
        format(users_saved, timestamp_before, timestamp_after)
    print(message)
    return users_saved
