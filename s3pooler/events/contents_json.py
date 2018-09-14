# Seção responsável por criar os dicionário JSON para serem guardados
# Todas as funções devem receber um JSON do evento e retornar o JSON com
# o conteúdo, exemplo :

def _dict(callback, keys_list):
    return {key:callback(key) for key in keys_list}

def common_json(json_model):
    return {'response_code': json_model.code()}

def comment_json(json_model):
     comment_json = common_json(json_model)
     comment_json['message'] = json_model.request('message')
     return comment_json

def user_json(json_model):
    user_json = common_json(json_model)
    keys = ['facebook_id','instagram_id','about_me','image_profile']
    user_json.update(_dict(json_model.response, keys))
    return user_json

def post_json(json_model):
    post_json = common_json(json_model)
    keys = ['post_type','title','text','tags','user_mark','images']
    post_json.update(_dict(json_model.request, keys))
    return post_json

def reaction_json(json_model):
    react_json = common_json(json_model)
    react_json['reaction_code'] =json_model.request('liked')
    return react_json

def scroll_json(json_model):
    scroll_json = common_json(json_model)
    scroll_json['page'] = json_model.string_params('page')
    return scroll_json
