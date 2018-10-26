from django.apps import AppConfig

class YummieConfig(AppConfig):
    name = 'yummie'

    def ready(self):
        import yummie.events.events_router 
        from s3pooler.loader import Loader
        from .visions import RawVision, UsersVision
        visions_in_order = [RawVision, UsersVision]
        Loader().start_pooler(visions_in_order)