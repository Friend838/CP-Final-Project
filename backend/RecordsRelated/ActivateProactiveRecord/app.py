import boto3
import json

from datetime import datetime
from exception_utili import *

client = boto3.client('iot-data')


def lambda_handler(event, context):
    
    try:
        '''
        validate payload
        '''
        payload = json.loads(event['body'])
        if not validate_payload(payload):
            raise BodyParamsError('too less')
        
        if not validate_additional_payload(payload):
            raise BodyParamsError('too many')
        
        payload['timestamp'] = str(int(datetime.utcnow().timestamp()))
        payload['action'] = 'manual_activate'
        
        client.publish(
            topic='team16/fp',
            qos=0,
            payload=json.dumps(payload)
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "statusCode": 200,
                "body": 'payload: "{}" publish to mqtt successfully'.format(payload)
            })
        }
        
    except BodyParamsError as bpe:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "statusCode": 500,
                "body": bpe.message
            })
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "statusCode": 500,
                "body": str(e)
            })
        }
        