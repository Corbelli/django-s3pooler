from s3pooler.events.events_router import router
from s3pooler.utils.event_json import get_path, get_code, get_request, get_response
from s3pooler.models import EventPaths, UsersEvents

class EventsJSONProcessor:
    def translate_modellist(self, s3_json_models):
        models = [self.__procces_model(json_model) for json_model in s3_json_models]
        return [model for model in models if model != None]

    def __procces_model(self, json_model):
        model = None
        event_dict = router.get(json_model.path())
        if event_dict.get('callback', None):
           model = event_dict['callback'](json_model)
           if model.event_type == '':
            model.event_type = event_dict['event']
        return model

class EventsProcessor:
    def translate_modellist(self, event_models, table):
        models = [self.__procces_model(event_model, table) for event_model in event_models]
        return [model for model in models if model != None]

    def __procces_model(self, model, table):
        return table(
            timestamp=model.timestamp,
            name=model.name,
            event_type=model.event_type,
            event_id=model.event_id,
            user_id=model.user_id,
            content=model.content,
            target_type=model.target_type,
            target_id=model.target_id,
            referal=model.referal,
            os=model.referal,
            device=model.device,
            identifier=model.identifier
        )

class PathsProcessor:
    paths = {}

    def update_save_paths(self, s3_json_models):
        [self.__save_json_pathdict(json_model) for json_model in s3_json_models]
        self.__update_saved_paths_table()

    def __save_json_pathdict(self, json_model):
        event_dict = router.get(json_model.path)
        path = event_dict.get('pure_path', json_model.path)
        self.paths[path] = {'request': json_model.request,
                            'response': json_model.response}

    def __update_saved_paths_table(self):
        saved_events = EventPaths.objects.get_events()
        processed_events = {path:{'registered': router.has(path),
                                  'request': path_dict['request'],
                                  'response': path_dict['response']}
                    for path, path_dict in self.paths.items()}
        for path, route_dict in processed_events.items():
            saved_events[path] = route_dict
        EventPaths.objects.save_events(saved_events)
