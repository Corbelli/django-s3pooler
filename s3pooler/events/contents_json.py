# importa funções de auxilio para ler o JSON de evento no S3
from s3pooler.utils.event_json import get_created_at, get_headers, get_request, get_response_data

# Seção responsável por criar os dicionário JSON para serem guardados
# Todas as funções devem receber um JSON do evento e retornar o JSON com
# o conteúdo, exemplo :

# def user_json(event_json):
#     user_json = {}
#     response = get_response_data(event_json)
#     user_json['facebook_id'] = response.get('facebook_id', '')
#     user_json['instagram_id'] = response.get('instagram_id', '')
#     user_json['about_me'] = response.get('about_me', '')
#     user_json['image_profile'] = response.get('image_profile', '')
#     user_json['instagram_id'] = response.get('instagram_id', '')
#     return user_json
