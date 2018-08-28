from s3pooler.models import Events
from datetime import datetime, timedelta, timezone
from django.db import transaction
import environ
import pytz
import json
import boto3
from functools import reduce
env = environ.Env()

class Pooler():

    client = boto3.client('s3',
                aws_access_key_id=env.str('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=env.str('AWS_SECRET_ACCESS_KEY'),
                )
    session = boto3.Session(
                aws_access_key_id=env.str('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=env.str('AWS_SECRET_ACCESS_KEY'),
                )
    s3 = session.resource('s3')
    bucket_name = env.str('AWS_S3_BUCKET_NAME')
    bucket = s3.Bucket(bucket_name)
    firehose_name = env.str('AWS_FIREHOSE_NAME')

    def get_last_timestamp(self):
        return Events.objects.last_timestamp()

    def get_recent_files(self, last_timestamp):
        files = list(self.bucket.objects.all())
        s3_keys_already_processed = Events.objects.get_last_timestamp_s3_keys()
        if (last_timestamp is None) or (s3_keys_already_processed is None):
            return [_file.key for _file in files]
        return [_file.key for _file in files \
                if (self.__get_key_first_event_time(_file.key)  >= last_timestamp) and \
                   (self.__get_key_id(_file.key) not in s3_keys_already_processed) ]

    def get_entries(self, keys):
        entries_lists = [self.__get_key_entries(key) for key in keys]
        entries_list = reduce((lambda x, y: x + y), entries_lists, [])
        return entries_list

    @transaction.atomic
    def save_models(self, models):
        for model in models:
            model.save()

    def __get_key_entries(self, key):
        api_response = self.client.select_object_content(
            Bucket= self.bucket_name,
            Key= key,
            ExpressionType='SQL',
            Expression= 'select * from s3object s ',
            InputSerialization = {'CompressionType': 'GZIP', 'JSON': {'Type': 'Document'}},
            OutputSerialization = {'JSON': {'RecordDelimiter': '\n',}},
            )
        return self.__s3_response_to_jsonlist(api_response, key)

    def __s3_response_to_jsonlist(self, api_response, key):
        if 'Payload' not in api_response:
            raise Exception('Failed to get key : {}'.format(key))
        events = list(api_response['Payload'])
        records = [event for event in events if 'Records' in event]
        jsons_string = [record['Records']['Payload'].decode('utf-8') for record in records]
        jsons = [json.loads(string) for string in jsons_string[0].split('\n') if string != '']
        jsons = self.__ad_key_id(key, jsons)
        return jsons

    def __ad_key_id(self, key, jsons):
        key_id = self.__get_key_id(key)
        for _json in jsons:
            _json['s3_key_id'] = key_id
        return jsons

    def __get_key_id(self, key):
        key_without_name = key.replace(self.firehose_name + '-', '')
        random_codes = key_without_name.split('-')[7:]
        random_code_gz = reduce((lambda x, y: x + '-' + y), random_codes)
        return random_code_gz[:-3]

    def __get_key_first_event_time(self, key):
        key_without_name = key.replace(self.firehose_name + '-', '')
        date_string = key_without_name.split('-')[1:7]
        date = datetime(year=int(date_string[0]), month=int(date_string[1]), day=int(date_string[2]),\
               hour=int(date_string[3]), minute=int(date_string[4]), second=int(date_string[5]), tzinfo=pytz.UTC)
        return date
