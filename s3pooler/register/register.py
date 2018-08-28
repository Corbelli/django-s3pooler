from s3pooler.register.pooler import Pooler
from s3pooler.events.events_router import router
from s3pooler.utils.event_json import get_path, get_code

class EventsRegister(Pooler):

    def procces_events(self, s3_jsons):
        models = [self.__procces_event(event_json) for event_json in s3_jsons]
        models = [model for model in models if model != None]
        return models

    def __procces_event(self, s3_event_json):
        model = None
        if get_path(s3_event_json) in router and \
        get_code(s3_event_json) == 200:
           event_callback = router[get_path(s3_event_json)]
           model = event_callback(s3_event_json)
        return model
