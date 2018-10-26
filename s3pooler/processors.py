from s3pooler.router import Router
from s3pooler.models import EventPaths

router = Router()
class PathsProcessor:
    paths = {}

    def update_save_paths(self, models):
        [self.__save_json_pathdict(json_model) for json_model in models]
        self.__update_saved_paths_table()

    def __save_json_pathdict(self, json_model):
        event_dict = router.get(json_model.path())
        path = event_dict.get('pure_path', json_model.path())
        self.paths[path] = {'request': json_model.request(),
                            'response': json_model.response()}

    def __update_saved_paths_table(self):
        saved_events = EventPaths.objects.get_events()
        processed_events = {path:{'registered': router.has(path),
                                  'request': path_dict['request'],
                                  'response': path_dict['response']}
                    for path, path_dict in self.paths.items()}
        for path, route_dict in processed_events.items():
            saved_events[path] = route_dict
        EventPaths.objects.save_events(saved_events)
class EventsJSONProcessor:
    paths_saver = PathsProcessor()

    def translate_modellist(self, s3_json_models):
        self.paths_saver.update_save_paths(s3_json_models)
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

class SameModelProcessor:
    def translate_modellist(self, event_models, table):
        models = [self.__procces_model(event_model, table) for event_model in event_models]
        return [model for model in models if model != None]

    def __procces_model(self, model, table):
        new_model = table()
        for field in model._meta.fields:
            if not field.primary_key:
                setattr(new_model, field.name, getattr(model, field.name))
        return new_model
