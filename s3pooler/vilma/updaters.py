import logging
from s3pooler.vilma.s3scrapper import S3Scrapper
from django.db import transaction
from s3pooler.models import Datetimes
from s3pooler.vilma.processors import EventsJSONProcessor, PathsProcessor
from s3pooler.vilma.pooler import Pooler


scrapper = S3Scrapper()

async def update_json(files_to_scrap=5):
    timestamp_before = Datetimes.objects.last_timestamp('s3pooler')
    nr_registered = scrapper.scrapp_and_save(timestamp_before, files_to_scrap)
    timestamp_after = Datetimes.objects.last_timestamp('s3pooler')
    message = 'S3 {:3d} events scrapped, timestamp before: {} , after : {}'.\
        format(nr_registered, timestamp_before, timestamp_after)
    logging.info(message)
    return (timestamp_before, timestamp_after)

def main_factory(vision):
    async def update_main(timestamp_before=None, timestamp_after=None):
        if timestamp_after==None:
            timestamp_before = Datetimes.objects.last_timestamp('visions')
        raw_saved = vision.pool(timestamp_before, timestamp_after)
        message = 'Raw Updated, {} timestamp before: {} , after : {}'.\
            format(raw_saved, timestamp_before, timestamp_after)
        logging.info(message)
        return (timestamp_before, timestamp_after)
    return update_main    

def vision_factory(vision):
    async def update_users(timestamp_before=None, timestamp_after=None):
        users_saved = vision.pool(timestamp_before, timestamp_after)
        message = 'Users Updated, {}  timestamp before: {} , after : {}'.\
            format(users_saved, timestamp_before, timestamp_after)
        logging.info(message)
    return update_users
