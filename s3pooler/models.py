from django.db import models
from django_mysql.models import  Model
from django.contrib.postgres.fields import JSONField as PostgresJSONField
from django_mysql.models import JSONField as MySQLJSONField
import environ
env = environ.Env()

### Específico para MySQL ###

class EventsManager(models.Manager):

    def last_timestamp(self):
        last_event = self.order_by('-timestamp').first()
        if not last_event:
            return None
        return last_event.timestamp

    def get_last_timestamp_s3_keys(self):
        last_timestamp = self.last_timestamp()
        last_timestamp_events = self.filter(timestamp__exact=last_timestamp)
        if not last_timestamp_events:
            return None
        s3_keys_identifiers = [event.s3_key_id for event in last_timestamp_events]
        return set(s3_keys_identifiers)

is_mysql = (env.str('DB_ENGINE', '').split('.')[-1] == 'mysql')

class Events(Model if is_mysql else models.Model):

    REFERALS = (
        ('Email', 'Email'),
        ('Organic', 'Organic'),
        ('Push', 'Push'),
    )

    OSS = (
        ('Android', 'Android'),
        ('IOS', 'IOS'),
    )

    objects = EventsManager()

    timestamp = models.DateTimeField()
    event_type = models.CharField(max_length=25)
    event_id = models.BigIntegerField(null=True)
    user_id = models.BigIntegerField()
    user_name = models.CharField(max_length=50)
    content = MySQLJSONField(null=True) \
        if is_mysql else PostgresJSONField(null=True)
    target_type = models.CharField(max_length=20, null=True)
    target_id = models.BigIntegerField(null=True)
    referal = models.CharField(max_length=20, choices=REFERALS)
    os = models.CharField(max_length=20, choices=OSS)
    device = models.CharField(max_length=50, default='Undefined')
    s3_key_id = models.CharField(max_length=100, default='Undefined')
