from celery.decorators import periodic_task
from .register.register import EventsRegister
from datetime import datetime, timedelta, timezone
import pytz

@periodic_task(run_every=timedelta(seconds=10))
def track_changes5():
    register = EventsRegister()
    last_timestamp = register.get_last_timestamp()
    recent_files = register.get_recent_files(last_timestamp)
    events = register.get_entries(recent_files)
    models = register.procces_events(events)
    register.save_models(models)
    print('Task Done : {} events logged'.format(len(models)))
