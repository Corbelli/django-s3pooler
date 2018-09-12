from .pooler import Pooler
from s3pooler.models import JsonEvents, RawEvents, Datetimes
from .processors import EventsJSONProcessor, PathsProcessor

class RawVision:
    pooler = Pooler(JsonEvents)
    translator = EventsJSONProcessor()
    pahts_saver = PathsProcessor()

    def pool_save_update_tables(self, min_timestamp, max_timestamp):
        modellist = self.__events_in_timestamp_interval(min_timestamp, max_timestamp)
        translated = self.__translate_modellist(modellist)
        return self.__save_update_tables(modellist, translated, min_timestamp, max_timestamp)

    def __events_in_timestamp_interval(self, min_timestamp, max_timestamp):
        return self.pooler.events_in_timestamp_interval(self.__filter_func,
                                                        min_timestamp,
                                                        max_timestamp)

    def __translate_modellist(self, models_list):
        return self.translator.translate_modellist(models_list)

    def __save_update_tables(self, modellist, translated_modellist, min_timestamp, max_timestamp):
        self.pahts_saver.update_save_paths(modellist)
        if max_timestamp==None:
            last_timestamp = self.__get_max_timestamp(translated_modellist)
            Datetimes.objects.set_last_datetime('visions', last_timestamp)
        return self.pooler.save_models(translated_modellist, RawEvents)

    def __get_max_timestamp(self, models):
        return sorted(models, key=lambda model: model.timestamp)[-1].timestamp

    def __filter_func(self, query_set):
        return query_set
