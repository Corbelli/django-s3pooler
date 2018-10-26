import logging
import asyncio
from s3pooler.internal.s3scrapper import S3Scrapper
from django.db import transaction
from s3pooler.models import Datetimes, JsonEvents
from s3pooler.processors import EventsJSONProcessor, PathsProcessor
from s3pooler.pooler import Pooler


async def update_json(files_to_scrap=5):
    scrapper = S3Scrapper()
    timestamp_before = Datetimes.objects.last_timestamp('s3pooler')
    nr_registered = scrapper.scrapp_and_save(timestamp_before, files_to_scrap)
    timestamp_after = Datetimes.objects.last_timestamp('s3pooler')
    message = 'S3 {:3d} events scrapped, timestamp before: {} , after : {}'.\
        format(nr_registered, timestamp_before, timestamp_after)
    logging.info(message)
    return (timestamp_before, timestamp_after)

def main_factory(VisionClass):
    async def update_main(vision_id, timestamp_before=None, timestamp_after=None):
        if timestamp_after==None:
            timestamp_before = Datetimes.objects.last_timestamp('visions')
        vision = VisionClass()
        vision.timestamp_after = timestamp_after
        events_saved = vision.pool(timestamp_before, timestamp_after)
        message = 'Vision {} Updated, {}  new, timestamp before: {} , after : {}'.\
            format(vision_id, events_saved, timestamp_before, timestamp_after)
        logging.info(message)
        return (timestamp_before, timestamp_after)
    return update_main    

def vision_factory(VisionClass):
    async def update_users(vision_id, timestamp_before=None, timestamp_after=None):
        vision = VisionClass()
        events_saved = vision.pool(timestamp_before, timestamp_after)
        message = 'Vision {} Updated, {}  new, timestamp before: {} , after : {}'.\
            format(vision_id, events_saved, timestamp_before, timestamp_after)
        logging.info(message)
    return update_users

async def purge_jsonevents_table():
    nr_deletions, _dict = JsonEvents.objects.purge()
    message = 'JsonEvents older than 1 day cleaned : {}'.format(nr_deletions)
    logging.info(message)
    return nr_deletions
