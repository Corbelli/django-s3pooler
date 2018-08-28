import json
import pytz
from datetime import datetime

def get_request(event_json):
    return event_json['request']

def get_headers(event_json):
    return get_request(event_json)['headers']

def get_path(event_json):
    return event_json['request']['path']

def get_code(event_json):
    return event_json['response']['statusCode']

def get_response_data(event_json):
    return json.loads(event_json['response']['body'])['data']

def get_created_at(event_json):
    return string_to_datetime(event_json['timestamp'])

def string_to_datetime(time_string):
    return datetime.fromtimestamp(int(time_string))\
                    .replace(tzinfo=pytz.UTC)
