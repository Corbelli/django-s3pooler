from .vilma.s3scrapper import S3Scrapper
from .vilma.raw_vision import RawVision
from datetime import timedelta
from .models import Datetimes
from .visions import UsersVision
from django.db import transaction, connection

from datetime import datetime
import logging
import threading
import asyncio

async def scrapp_s3(files_to_scrap=5):
    scrapper = S3Scrapper()
    timestamp_before = Datetimes.objects.last_timestamp('s3pooler')
    nr_registered = scrapper.scrapp_save_update_datetime(timestamp_before, files_to_scrap)
    timestamp_after = Datetimes.objects.last_timestamp('s3pooler')
    message = 'S3 {:3d} events scrapped, timestamp before: {} , after : {}'.\
        format(nr_registered, timestamp_before, timestamp_after)
    logging.info(message)
    return (timestamp_before, timestamp_after)

async def update_raw(timestamp_before=None, timestamp_after=None):
    raw = RawVision()
    if timestamp_after==None:
        timestamp_before = Datetimes.objects.last_timestamp('visions')
    raw_saved = raw.pool_save_update_tables(timestamp_before, timestamp_after)
    message = 'Raw Updated, {} timestamp before: {} , after : {}'.\
        format(raw_saved, timestamp_before, timestamp_after)
    logging.info(message)
    return (timestamp_before, timestamp_after)

async def update_users(timestamp_before=None, timestamp_after=None):
    users = UsersVision()
    users_saved = users.pool_save(timestamp_before, timestamp_after)
    message = 'Users Updated, {}  timestamp before: {} , after : {}'.\
        format(users_saved, timestamp_before, timestamp_after)
    logging.info(message)
