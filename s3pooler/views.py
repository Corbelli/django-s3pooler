import pytz
from datetime import datetime
from .models import EventPaths, Datetimes, RawEvents
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .register.register import EventsRegister

@api_view(['POST'])
def set_scrapping_datetime(request):
    time_dict = request.data
    cmd = 'reset' if time_dict.get('reset', 0) else 'set'
    last_datetime = get_datetime(time_dict) if cmd == 'set' else None
    Datetimes.objects.set_last_datetime(RawEvents, last_datetime, cmd)
    return Response('Valor da tabela setado para {}'.format(last_datetime))

def get_datetime(time_dict):
    return datetime(
            time_dict['year'],time_dict['month'],time_dict['day'],\
            time_dict.get('hour',0),time_dict.get('minutes',0),\
            time_dict.get('seconds',0), tzinfo=pytz.UTC)

@api_view(['DELETE'])
def delete_paths(request):
    targets = request.data['starts_with']
    for target in targets:
        EventPaths.objects.filter(path__startswith=target).delete()
    return Response('Registros deletados')


