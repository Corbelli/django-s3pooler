# importa utilidades para queries nas tabelas específicas de dados
# do banco da aplicação
from s3pooler.events.application_db import get_username
# importa o modelo do banco de eventos
from s3pooler.models import RawEvents
# importa todas as funções para criação dos dicionários de JSONField
from s3pooler.events.contents_json import *
# Seção responsável por criar as funções específicas que sabem
# guardar cada evento. Aconselha-se criar um função para as informacões
# comuns a todos os eventos e uma para cada evento, exemplo :

def common(json_model):
    event = RawEvents()
    event.referal = json_model.headers('Referal')
    event.os = json_model.headers('OS')
    event.device = json_model.headers('Device-id')
    event.timestamp = json_model.timestamp
    event.identifier = json_model.identifier
    return event

def login(json_model):
    event = common(json_model)
    event.user_id = json_model.response('id', -1)
    event.name = get_username(event.user_id)
    event.content = user_json(json_model)
    return event

def user_created(json_model):
     event = common(json_model)
     event.event_id = json_model.response('id', -1)
     event.user_id = json_model.response('id', -1)
     event.name = get_username(event.user_id)
     event.content = user_json(json_model)
     return event

def post_reaction(json_model):
    event = common(json_model)
    if 'post_id' in json_model.request():
        event.target_id = json_model.request('post_id', -1)
        event.event_type = 'Post_Reaction'
        event.target_type = 'Post'
    if 'comment_id' in json_model.request():
        event.target_id = json_model.request('comment_id', -1)
        event.event_type = 'Comment_Reaction'
        event.target_type = 'Comment'
    event.user_id = json_model.request('user_id', -1)
    event.name = get_username(event.user_id)
    event.content = reaction_json(json_model)
    return event

def comment_reaction(json_model):
    event = common(json_model)
    event.target_type = 'Comment'
    event.target_id = json_model.request('comment_id', -1)
    event.user_id = json_model.request('user_id', -1)
    event.name = get_username(event.user_id)
    event.content = reaction_json(json_model)
    return event

def post_created(json_model):
    event = common(json_model)
    event.event_id = json_model.response('id', -1)
    event.user_id = json_model.response('user').get('id', -1)
    event.name = get_username(event.user_id)
    event.content = post_json(json_model)
    return event

def comment_created(json_model):
    event = common(json_model)
    event.user_id = json_model.request('user_id', -1)
    event.name = get_username(event.user_id)
    event.content = comment_json(json_model)
    event.target_type = 'Post'
    event.target_id = json_model.request('post_id', -1)
    return event

def feed_scrolled(json_model):
    event = common(json_model)
    event.user_id = json_model.string_params('user_id', -1)
    event.name = get_username(event.user_id)
    event.content = common_json(json_model)
    return event

def accepted_follow(json_model):
    event = common(json_model)
    event.user_id = json_model.request('user_id', -1)
    event.name = get_username(event.user_id)
    event.target_id = json_model.request('friend_id', -1)
    event.target_type = 'User'
    event.content = common_json(json_model)
    return event

def follow_request(json_model):
    event = common(json_model)
    event.user_id = json_model.request('user_id', -1)
    event.name = get_username(event.user_id)
    event.target_id = json_model.request('following_id', -1)
    event.target_type = 'User'
    event.content = common_json(json_model)
    return event
