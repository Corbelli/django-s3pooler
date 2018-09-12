import pytz
from .pooler import Pooler
from datetime import datetime
from .s3manager import S3Manager
from django.db import transaction
from s3pooler.models import JsonEvents, Datetimes


class S3Scrapper:
    s3 = S3Manager()
    pooler = Pooler(None)

    def scrapp_save_update_datetime(self, last_timestamp, nr_files):
        sorted_objs = self.s3.get_recent_objs(last_timestamp, nr_files)
        last_modified = sorted_objs[-1].modified_at
        jsonlist = self.s3.get_keylist_jsons([obj.key for obj in sorted_objs])
        models = [self.__process_json(json) for json in jsonlist]
        return self.__save_models_update_datetime(models, last_modified)

    @transaction.atomic
    def __save_models_update_datetime(self, modelslist, last_modified):
        Datetimes.objects.set_last_datetime(last_modified)
        return self.pooler.save_models(modelslist, JsonEvents)

    def __process_json(self, json):
        return JsonEvents(timestamp=self.__string_to_datetime(json['timestamp']),
                   request=json['request'],
                   response=json['response'])

    def __string_to_datetime(self, time_string):
        return datetime.fromtimestamp(int(time_string))\
                        .replace(tzinfo=pytz.UTC)
