import pytz
import json
import time
import boto3
import environ
from io import BytesIO
from gzip import GzipFile
from functools import reduce
from datetime import datetime, timedelta
env = environ.Env()
MAX_OBJS_TO_GET = 1000

class S3Manager():
    bucket_name = env.str('AWS_S3_BUCKET_NAME')
    firehose_name = env.str('AWS_FIREHOSE_NAME')
    client = boto3.client('s3',
                aws_access_key_id=env.str('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=env.str('AWS_SECRET_ACCESS_KEY'),
                )
    bucket = boto3.Session(
                aws_access_key_id=env.str('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=env.str('AWS_SECRET_ACCESS_KEY'),
                ).resource('s3').Bucket(bucket_name)

    def __get_search_dates(self, date):
        if date is None:
            return {}
        hour_ahead = date + timedelta(hours=1)
        day_ahead = date + timedelta(days=1)
        hour = '{}/{:02d}/{:02d}/{:02d}/'.format(date.year, date.month, date.day, date.hour)
        next_hour = '{}/{:02d}/{:02d}/{:02d}/'.format(hour_ahead.year, hour_ahead.month, hour_ahead.day, hour_ahead.hour)
        day = '{}/{:02d}/{:02d}/'.format(date.year, date.month, date.day)
        next_day = '{}/{:02d}/{:02d}/'.format(day_ahead.year, day_ahead.month, day_ahead.day)
        return {'hour':hour, 'next_hour':next_hour, 'day':day, 'next_day':next_day}

    def __get_recent_in_search(self, last_timestamp, search):
        objs = self.bucket.objects.limit(MAX_OBJS_TO_GET) if search == None \
        else self.bucket.objects.filter(Prefix=search).limit(MAX_OBJS_TO_GET)
        return list(objs) if (last_timestamp is None) else \
        [_file for _file in objs if _file.last_modified  > last_timestamp]

    def get_recent_objs(self, last_timestamp, n_files_to_process):
        ''' Pega os n_files_to_procces arquivos mais antigos entre todos
        os arquivos no bucket com eventos mais recentes que last_timestamp'''
        search = self.__get_search_dates(last_timestamp)
        recent_objs = self.__get_recent_in_search(last_timestamp, search.get('hour'))
        if (len(recent_objs) == 0) and current_is_one_hour_ahead(last_timestamp):
            recent_objs = self.__get_recent_in_search(last_timestamp, search.get('next_hour'))
            if (len(recent_objs) == 0):
                recent_objs = self.__get_recent_in_search(last_timestamp, search.get('day'))
                if (len(recent_objs) == 0):
                    recent_objs = self.__get_recent_in_search(last_timestamp, search.get('next_day'))
        return self.__get_first_n_recent_objects(recent_objs, n_files_to_process)

    def get_keylist_jsons(self, keys):
        '''Devolve uma lista de dicts com todos os eventos presentes em todos
        os objetos passados'''
        entries_lists = [self.__get_key_jsonlist(key) for key in keys]
        return reduce((lambda x, y: x + y), entries_lists, [])

    def __get_first_n_recent_objects(self, recent_objects, n):
        sorted_objs = sorted(recent_objects, key=lambda obj: obj.last_modified)
        nr_keys = (n + 1) if (n+1 <= len(sorted_objs)) else len(sorted_objs)
        return sorted_objs[:nr_keys]

    def __get_key_jsonlist(self, key):
        api_response = self.client.get_object(
            Bucket= self.bucket_name,
            Key= key,
        )
        return self.__s3_response_to_jsonlist(api_response, key)

    def __s3_response_to_jsonlist(self, api_response, key):
        bytestream = BytesIO(api_response['Body'].read())
        events_text = GzipFile(None, 'rb', fileobj=bytestream).read().decode('utf-8')
        events_str_list = events_text.replace('}{', '}JSON_STRING_DELIMITER{')\
                    .split('JSON_STRING_DELIMITER')
        jsons = [json.loads(string) for string in events_str_list]
        return jsons

def time_since(datetime):
    return datetime.utcnow().replace(tzinfo=pytz.utc) - datetime

def current_is_one_hour_ahead(last_datetime):
    return datetime.utcnow().replace(tzinfo=pytz.utc) > last_datetime\
        .replace(minute=0,second=0) + timedelta(hours=1)
