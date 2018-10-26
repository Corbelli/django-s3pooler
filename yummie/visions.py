from .constants import BLACKLIST
from s3pooler.models import JsonEvents
from s3pooler.pooler import Pooler
from .models import RawEvents, UsersEvents
from s3pooler.processors import SameModelProcessor, EventsJSONProcessor, PathsProcessor

class UsersVision():
    pooler = Pooler(RawEvents)
    processor = SameModelProcessor()

    def pool(self, min_timestamp, max_timestamp):
        modellist = self.pooler.events_in_timestamp_interval(self.__exclude_blacklist,
                            min_timestamp, max_timestamp)
        translated_modellist = self.processor.translate_modellist(modellist, UsersEvents)
        return self.pooler.save_models(translated_modellist, UsersEvents)

    def __exclude_blacklist(self, query_set):
        return query_set.exclude(user_id__in=BLACKLIST)

class RawVision:
    pooler = Pooler(JsonEvents)
    translator = EventsJSONProcessor()

    def pool(self, min_timestamp, max_timestamp):
        modellist = self.pooler.events_in_timestamp_interval(self.__filter_func, min_timestamp, max_timestamp)
        translated_modellist = self.translator.translate_modellist(modellist)
        return self.pooler.save_models(translated_modellist, RawEvents)

    def __filter_func(self, query_set):
        return query_set
