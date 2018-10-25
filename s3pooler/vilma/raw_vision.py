from .pooler import Pooler
from s3pooler.models import JsonEvents, RawEvents, Datetimes
from .processors import EventsJSONProcessor, PathsProcessor
from django.db import transaction

class RawVision:
    pooler = Pooler(JsonEvents)
    translator = EventsJSONProcessor()
    paths_saver = PathsProcessor()

    def pool(self, min_timestamp, max_timestamp):
        modellist = self.pooler.events_in_timestamp_interval(self.__filter_func, min_timestamp, max_timestamp)
        translated = self.translator.translate_modellist(modellist)
        return self.pooler.save_models_main_vision(modellist, translated, max_timestamp, RawEvents)

    def __filter_func(self, query_set):
        return query_set
