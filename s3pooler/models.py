from django.db import models
from django_mysql.models import  Model
from django.contrib.postgres.fields import JSONField as PostgresJSONField
from django_mysql.models import JSONField as MySQLJSONField
import environ
env = environ.Env()

### Específico para MySQL ###
is_mysql = (env.str('DB_ENGINE', '').split('.')[-1] == 'mysql')

class JsonEvents(models.Model):
    timestamp = models.DateTimeField()
    request = MySQLJSONField() \
        if is_mysql else PostgresJSONField()
    response = MySQLJSONField() \
        if is_mysql else PostgresJSONField()
    inserted_at = models.DateTimeField(auto_now_add=True)

class Events(Model if is_mysql else models.Model):
    timestamp = models.DateTimeField()
    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=25)
    event_id = models.BigIntegerField(null=True)
    user_id = models.BigIntegerField()
    content = MySQLJSONField(null=True) \
        if is_mysql else PostgresJSONField(null=True)
    target_type = models.CharField(max_length=20, null=True)
    target_id = models.BigIntegerField(null=True)
    referal = models.CharField(max_length=20, default='Undefined')
    os = models.CharField(max_length=20, default='Undefined')
    device = models.CharField(max_length=50, default='Undefined')
    identifier = models.CharField(max_length=100)
    class Meta:
        abstract = True
        indexes = [
           models.Index(fields=['-timestamp','event_type']),
           models.Index(fields=['event_type']),
        ]

class RawEvents(Events):
    pk_id = models.AutoField(primary_key=True)
class UsersEvents(Events):
    pk_id = models.AutoField(primary_key=True)

class DatetimeManager(models.Manager):
    def last_timestamp(self, function):
        last_event = self.filter(function=function).first()
        return last_event.last_processed_timestamp if last_event else None
    def clean_last_datetime(self, function):
        self.filter(function=function).delete()
    def set_last_datetime(self, function, datetime=None, cmd=None):
        self.clean_last_datetime(function)
        if cmd == 'reset':
            return
        last_datetime = self.last_timestamp(function)
        if (not last_datetime) or cmd or (not last_datetime.command):
            self.create(last_processed_timestamp=datetime,
                        command=cmd,
                        function=function)
        elif last_datetime.command == 'set':
            last_datetime.command = None
            last_datetime.save()
        return

class Datetimes(models.Model):
    objects = DatetimeManager()
    last_processed_timestamp = models.DateTimeField(null=True, blank=True)
    command = models.CharField(max_length=20, null=True)
    function = models.CharField(max_length=20, null=True)

class EventsPathManager(models.Manager):
    def get_events(self):
        return {event.path:{'registered':event.registered,
                            'request': event.request,
                            'response': event.response} for event in
            list(self.all())}
    def save_events(self,events_dict):
        events = self.get_events()
        for path, route_dict in events_dict.items():
            if path not in events.keys():
                self.create(path=path, registered=route_dict['registered'],\
                    request=route_dict['request'],response=route_dict['response'])
            else:
                if route_dict['registered'] != events[path]['registered']:
                    self.filter(path=path).update(registered=route_dict['registered'])

class EventPaths(models.Model):
    objects = EventsPathManager()
    path = models.CharField(max_length=2000)
    registered = models.BooleanField()
    request = MySQLJSONField(null=True) \
        if is_mysql else PostgresJSONField(null=True)
    response = MySQLJSONField(null=True) \
        if is_mysql else PostgresJSONField(null=True)
