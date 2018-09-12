# importa utilidades para queries nas tabelas específicas de dados
# do banco da aplicação
from s3pooler.events.application_db import get_username
# importa o modelo do banco de eventos
from s3pooler.models import RawEvents
# importa todas as funções para criação dos dicionários de JSONField
from s3pooler.events.contents_json import *
# importa funções de auxilio para ler o JSON de evento no S3
from s3pooler.utils.event_json import get_created_at, get_headers,\
    get_request, get_response, get_path, get_id, get_request_response,\
    get_string_params
# Seção responsável por criar as funções específicas que sabem
# guardar cada evento. Aconselha-se criar um função para as informacões
# comuns a todos os eventos e uma para cada evento, exemplo :

def common(event_json):
    event = RawEvents()
    headers = get_headers(event_json)
    event.referal = headers.get('Referal', 'Undefined')
    event.os = headers.get('OS', 'Undefined')
    event.device = headers.get('Device-id', 'Undefined')
    event.timestamp = get_created_at(event_json)
    event.identifier = get_id(event_json)
    return event

def login(event_json):
    event = common(event_json)
    response = get_response(event_json)
    event.user_id = response.get('id', -1)
    event.name = get_username(event.user_id)
    event.content = user_json(event_json)
    return event

def user_created(event_json):
    event = common(event_json)
    response = get_response(event_json)
    event.event_id = response.get('id', -1)
    event.user_id = response.get('id', -1)
    event.name = get_username(event.user_id)
    event.content = user_json(event_json)
    return event

def post_reaction(event_json):
    event = common(event_json)
    request = get_request(event_json)
    if 'post_id' in request:
        event.target_id = request['post_id']
        event.event_type = 'Post_Reaction'
        event.target_type = 'Post'
    if 'comment_id' in request:
        event.target_id = request['comment_id']
        event.event_type = 'Comment_Reaction'
        event.target_type = 'Comment'
    event.user_id = request.get('user_id', -1)
    event.name = get_username(event.user_id)
    event.content = reaction_json(event_json)
    return event

def comment_reaction(event_json):
    event = common(event_json)
    request = get_request(event_json)
    event.target_type = 'Comment'
    event.target_id = request.get('comment_id', -1)
    event.user_id = request.get('user_id', -1)
    event.name = get_username(event.user_id)
    event.content = reaction_json(event_json)
    return event

def post_created(event_json):
    event = common(event_json)
    response = get_response(event_json)
    event.event_id = response.get('id', -1)
    event.user_id = response['user']['id']
    event.name = get_username(event.user_id)
    event.content = post_json(event_json)
    return event

def comment_created(event_json):
    event = common(event_json)
    request, response = get_request_response(event_json)
    event.user_id = request.get('user_id', -1)
    event.name = get_username(event.user_id)
    event.content = comment_json(event_json)
    event.target_type = 'Post'
    event.target_id = request.get('post_id', -1)
    return event

def feed_scrolled(event_json):
    event = common(event_json)
    event.user_id = get_string_params(event_json).get('user_id', -1)
    event.name = get_username(event.user_id)
    event.content = common_json(event_json)
    return event

def accepted_follow(event_json):
    event = common(event_json)
    request = get_request(event_json)
    event.user_id = request.get('user_id', -1)
    event.name = get_username(event.user_id)
    event.target_id = request.get('friend_id', -1)
    event.target_type = 'User'
    event.content = common_json(event_json)
    return event

def follow_request(event_json):
    event = common(event_json)
    request = get_request(event_json)
    event.user_id = request.get('user_id', -1)
    event.name = get_username(event.user_id)
    event.target_id = request.get('following_id', -1)
    event.target_type = 'User'
    event.content = common_json(event_json)
    return event
