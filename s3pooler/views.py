import pytz
from datetime import datetime
from .models import EventPaths, Datetimes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .apps import  S3PoolerConfig
import logging

@api_view(['POST'])
def set_s3pooler_datetime(request):
    return set_datetime(request, 's3pooler')

@api_view(['POST'])
def set_visions_datetime(request):
    S3PoolerConfig.views_update = True
    return set_datetime(request, 'visions')

@api_view(['DELETE'])
def delete_paths(request):
    targets = request.data['starts_with']
    for target in targets:
        EventPaths.objects.filter(path__startswith=target).delete()
    return Response('Registros deletados')

def set_datetime(request, associated_table):
    time_dict = request.data
    cmd = 'reset' if time_dict.get('reset', 0) else 'set'
    last_datetime = get_datetime(time_dict) if cmd == 'set' else None
    Datetimes.objects.set_last_datetime(associated_table, last_datetime, cmd)
    return Response('Valor da tabela setado para {}'.format(last_datetime))

def get_datetime(time_dict):
    return datetime(
            time_dict['year'],time_dict['month'],time_dict['day'],\
            time_dict.get('hour',0),time_dict.get('minutes',0),\
            time_dict.get('seconds',0), tzinfo=pytz.UTC)
