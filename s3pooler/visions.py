from .models import RawEvents, UsersEvents
from .constants import EVENTS_TO_LOG, BLACKLIST
from .vilma.pooler import Pooler
from .vilma.processors import EventsProcessor

class UsersVision():
    pooler = Pooler(RawEvents)
    processor = EventsProcessor()

    def pool_save(self, min_timestamp, max_timestamp):
        modellist = self.pooler.events_in_timestamp_interval(self.__exclude_blacklist,
                            min_timestamp, max_timestamp)
        translated_modellist = self.processor.translate_modellist(modellist, UsersEvents)
        return self.pooler.save_models(translated_modellist, UsersEvents)

    def __exclude_blacklist(self, query_set):
        return query_set.exclude(user_id__in=BLACKLIST)
