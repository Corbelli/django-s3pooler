# importa o modelo do banco de eventos
from s3pooler.models import Events
# importa todas as funções para criação dos dicionários de JSONField
from s3pooler.events.contents_json import *
# importa funções de auxilio para ler o JSON de evento no S3
from s3pooler.utils.event_json import get_created_at, get_headers,\
    get_request, get_response_data, get_path

# Seção responsável por criar as funções específicas que sabem
# guardar cada evento. Aconselha-se criar um função para as informacões
# comuns a todos os eventos e uma para cada evento, exemplo :

# def common(event_json):
#     event = Events()
#     headers = get_headers(event_json)
#     event.referal = headers.get('Referal', 'Undefined')
#     event.os = headers.get('OS', 'Undefined')
#     event.device = headers.get('Device-id', 'Undefined')
#     event.s3_key_id = event_json['s3_key_id']
#     event.timestamp = get_created_at(event_json)
#     return event

# def login(event_json):
#     event = common(event_json)
#     event.event_type = 'Login'
#     response = get_response_data(event_json)
#     event.user_name = response['name']
#     event.user_id = response['id']
#     return event
