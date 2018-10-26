import json
from django.db import models
from django_mysql.models import  Model
from django.contrib.postgres.fields import JSONField as PostgresJSONField
from django_mysql.models import JSONField as MySQLJSONField
import environ
env = environ.Env()

is_mysql = (env.str('EV_DB_ENGINE', '').split('.')[-1] == 'mysql')

class Events(Model if is_mysql else models.Model):
    timestamp = models.DateTimeField()
    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=25)
    event_id = models.BigIntegerField(null=True)
    user_id = models.BigIntegerField()
    user_created_at = models.DateTimeField(null=True)
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
