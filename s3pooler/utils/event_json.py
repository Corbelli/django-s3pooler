import json
import pytz
from datetime import datetime

def get_request(event_json):
    try:
        return json.loads(event_json['request']['body'])
    except Exception as e:
        return {'error': 'Could not get request body : {}'.format(str(e))}

def get_request_response(event_json):
    return (get_request(event_json), get_response(event_json))

def get_headers(event_json):
    return event_json['request']['headers']

def get_path(event_json):
    return event_json['request']['path']

def get_code(event_json):
    return event_json['response']['statusCode']

def get_response(event_json):
    try:
        return json.loads(event_json['response']['body'])['data']
    except Exception as e:
        return {'error': 'Could not get response body : {}'.format(str(e))}

def get_string_params(event_json):
    return event_json['request']['queryStringParameters']

def get_created_at(event_json):
    return string_to_datetime(event_json['timestamp'])

def string_to_datetime(time_string):
    return datetime.fromtimestamp(int(time_string))\
                    .replace(tzinfo=pytz.UTC)

def get_id(event_json):
    return event_json['request']['requestContext']['requestId']
