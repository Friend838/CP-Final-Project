import json
import boto3
import traceback
from datetime import datetime

iot_client = boto3.client('iot-data')

class BodyParamsError(Exception):
    # two types: "too less" or "too many" params
    def __init__(self, type):
        if type == 'too less':
            self.message = 'body params must have the following attributes: 1. "userId", 2. "taskName"'
        elif type == 'too many':
            self.message = 'body params only allow the following attributes: 1. "userId", 2. "taskName"'


def lambda_handler(event, context):
    try:
        payload = json.loads(event['body'])
        
        for key in payload.keys():
            if key not in ['userId', 'taskName']:
                raise BodyParamsError('too many')
        
        for key in ['userId', 'taskName']:
            if key not in payload.keys():
                raise BodyParamsError('too less')
            
        mqtt_payload = json.dumps(
            {
                'userId': payload['userId'],
                'action': 'assign_task_name',
                'taskName': payload['taskName'],
            }
        )
        
        iot_client.publish(
            topic='team16/fp',
            payload=mqtt_payload
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "statusCode": 200,
                "body": 'payload: "{}" publish successfully'.format(mqtt_payload)
            })
        }
    
    except BodyParamsError as bpe:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "statusCode": 500,
                "body": str(bpe.message)
            })
        }
    
    except Exception as err:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "statusCode": 500,
                "body": str(err)
            })
        }