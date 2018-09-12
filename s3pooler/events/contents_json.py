# importa funções de auxilio para ler o JSON de evento no S3
from s3pooler.utils.event_json import get_created_at, get_headers, get_request,\
get_response, get_code, get_string_params

# Seção responsável por criar os dicionário JSON para serem guardados
# Todas as funções devem receber um JSON do evento e retornar o JSON com
# o conteúdo, exemplo :

def common_json(json_model):
    common_json = {}
    common_json['response_code'] = json_model.code()
    return common_json

def comment_json(event_json):
    comment_json = common_json(event_json)
    comment_json['message'] = get_request(event_json)['message']
    return comment_json

def user_json(json_model):
    user_json = common_json(json_model)
    user_json['facebook_id'] = json_model.response('facebook_id', '')
    user_json['instagram_id'] = json_model.response('instagram_id', '')
    user_json['about_me'] = json_model.response('about_me', '')
    user_json['image_profile'] = json_model.response('image_profile', '')
    user_json['instagram_id'] = json_model.response('instagram_id', '')
    return user_json

def post_json(event_json):
    post_json = common_json(event_json)
    request = get_request(event_json)
    post_json['post_type'] = request.get('post_type', '')
    post_json['title'] = request.get('title', '')
    post_json['text'] = request.get('text', '')
    post_json['tags'] = request.get('tags', '')
    post_json['user_mark'] = request.get('user_mark', '')
    post_json['images'] = request.get('images', '')
    return post_json

def reaction_json(event_json):
    react_json = common_json(event_json)
    request = get_request(event_json)
    react_json['reaction_code'] =request['liked']
    return react_json

def scroll_json(event_json):
    scroll_json = common_json(event_json)
    scroll_json['page'] = get_string_params(event_json).get('page', 0)
    return scroll_json
