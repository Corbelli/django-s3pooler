import pytz
import json
import boto3
import environ
from io import BytesIO
from gzip import GzipFile
from functools import reduce
from datetime import datetime
env = environ.Env()

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

    def get_recent_objs(self, last_timestamp, n_files_to_process):
        ''' Pega os n_files_to_procces arquivos mais antigos entre todos
        os arquivos no bucket com eventos mais recentes que last_timestamp'''
        objs = list(self.bucket.objects.all())
        if (last_timestamp is None):
            recent_objs =  objs
        else:
            recent_objs = [_file for _file in objs \
                    if (self.__get_key_first_event_time(_file.key)  >= last_timestamp) ]
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

    def __get_key_first_event_time(self, key):
        key_without_name = key.replace(self.firehose_name + '-', '')
        date_string = key_without_name.split('-')[1:7]
        date = datetime(year=int(date_string[0]), month=int(date_string[1]), day=int(date_string[2]),\
               hour=int(date_string[3]), minute=int(date_string[4]), second=int(date_string[5]), tzinfo=pytz.UTC)
        return date
