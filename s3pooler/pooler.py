from django.db import transaction
from s3pooler.models import Datetimes
from s3pooler.processors import EventsJSONProcessor, PathsProcessor
EVENTS_TO_POOL = 300

class Pooler():
    table = None
    paths_saver = PathsProcessor()

    def __init__(self, table):
        self.table = table

    def events_in_timestamp_interval(self, filter_func,
                min_timestamp=None, max_timestamp=None):
        filtered = filter_func(self.__get_in_timestamp(min_timestamp, max_timestamp))
        return list(filtered[:EVENTS_TO_POOL])

    @transaction.atomic
    def save_models_main_vision(self, modellist, translated_modellist, max_timestamp, table_to_save):
        self.paths_saver.update_save_paths(modellist)
        last_timestamp = self.__get_max_timestamp(translated_modellist)
        if max_timestamp==None and last_timestamp != None:
                Datetimes.objects.set_last_datetime('visions', last_timestamp)
        return self.save_models(translated_modellist,table_to_save)

    @transaction.atomic
    def save_models(self, models, table_to_save):
            sorted_models = sorted(models, key=lambda model: model.timestamp)
            same_time_models = list(table_to_save.objects\
                    .filter(timestamp__gte=sorted_models[0].timestamp) \
                    .filter(timestamp__lte=sorted_models[-1].timestamp)) \
                    if sorted_models else []
            same_time_ids = set([model.identifier for model in same_time_models])
            models = [model.save() for model in models \
                if model.identifier not in same_time_ids]
            return len(models)

    def __get_in_timestamp(self, min_timestamp, max_timestamp):
        if min_timestamp and max_timestamp:
            return self.table.objects.filter(timestamp__gte=min_timestamp) \
                .filter(timestamp__lte=max_timestamp)
        elif min_timestamp:
            return self.table.objects.filter(timestamp__gte=min_timestamp)
        else:
            return self.table.objects.all()

    def __get_max_timestamp(self, models):
        return sorted(models, key=lambda model: model.timestamp)[-1].timestamp \
            if len(models) != 0 else None
