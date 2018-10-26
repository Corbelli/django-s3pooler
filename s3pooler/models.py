import json
import pytz
from django.db import models
from datetime import datetime, timedelta
from django_mysql.models import  Model
from django.contrib.postgres.fields import JSONField as PostgresJSONField
from django_mysql.models import JSONField as MySQLJSONField
import environ
env = environ.Env()

### Específico para MySQL ###
is_mysql = (env.str('EV_DB_ENGINE', '').split('.')[-1] == 'mysql')

class JsonEventsManager(models.Manager):
    def purge(self):
        one_day_ago = datetime.utcnow().replace(tzinfo=pytz.utc) -  timedelta(days=1)
        return self.filter(inserted_at__lt=one_day_ago).delete()

def utc_now():
    return datetime.utcnow().replace(tzinfo=pytz.utc)

class JsonEvents(models.Model):

    objects = JsonEventsManager()

    def request(self, param=None, default='Undefined'):
        try:
            return json.loads(self.request_dict['body']).get(param, default)\
            if param else json.loads(self.request_dict['body'])
        except Exception:
            return {'error': 'Could not get request body : {}'.format(self.response_dict)}

    def response(self, param=None, default='Undefined'):
        try:
            return json.loads(self.response_dict.get('body', {})).get('data', {}).get(param, default)\
            if param else json.loads(self.response_dict['body']).get('data', {})
        except Exception:
            return {'error': 'Could not get request body : {}'.format(self.response_dict)}

    def headers(self, param, default='Undefined'):
        return self.request_dict.get('headers', {}).get(param, default) if param \
            else self.request_dict.get('headers', {})
    def path(self):
        return self.request_dict.get('path', 'Undefined')

    def code(self):
        return self.response_dict.get('statusCode', '-1')

    def string_params(self, param, default='Undefined'):
        return self.request_dict.get('queryStringParameters', {}).get(param, default) \
            if param and self.request_dict.get('queryStringParameters') is not None \
            else default


    timestamp = models.DateTimeField()
    request_dict = MySQLJSONField() \
        if is_mysql else PostgresJSONField()
    response_dict = MySQLJSONField() \
        if is_mysql else PostgresJSONField()
    inserted_at = models.DateTimeField(default=utc_now)
    identifier = models.CharField(max_length=100)
    class Meta:
            indexes = [models.Index(fields=['timestamp'])]

class DatetimeManager(models.Manager):
    def last_timestamp(self, associated_table):
        last_event = self.filter(associated_table=associated_table).first()
        return last_event.last_processed_timestamp if last_event else None
    def clean_last_datetime(self, associated_table):
        self.filter(associated_table=associated_table).delete()
    def set_last_datetime(self, associated_table, datetime=None, cmd=None):
        last_datetime = self.filter(associated_table=associated_table).first()
        self.clean_last_datetime(associated_table)
        if cmd == 'reset':
            return
        if (not last_datetime) or cmd or (not last_datetime.command):
            self.create(last_processed_timestamp=datetime,
                        command=cmd,
                        associated_table=associated_table)
        elif last_datetime.command == 'set':
            last_datetime.command = None
            last_datetime.save()
        return

class Datetimes(models.Model):
    objects = DatetimeManager()
    last_processed_timestamp = models.DateTimeField(null=True, blank=True)
    command = models.CharField(max_length=20, null=True)
    associated_table = models.CharField(max_length=20, null=True)

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
