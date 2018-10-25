import sys
import logging
from django.apps import AppConfig

class YummieConfig(AppConfig):
    name = 'yummie'

    def ready(self):
        from s3pooler.apps import Loader
        from .visions import RawVision, UsersVision
        from .events.events_router import router
        if 'runserver' in sys.argv:
            pooler = Loader()
            pooler.load_tasks(RawVision(), [UsersVision()])
            pooler.start() 