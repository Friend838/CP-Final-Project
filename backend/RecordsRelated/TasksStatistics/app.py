import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time
import datetime

tableName = 'team16_final_project_history_record'
dynamoDB_resource = boto3.resource('dynamodb')


class BodyParamsError(Exception):
    # two types: "too less" or "too many" params
    def __init__(self, type):
        if type == 'too less':
            self.message = 'body params must have the following attributes: 1. "userId", 2. "task_name"'


def lambda_handler(event, context):

    try:

        # validate payload
        payload = json.loads(event['body'])
        if 'userId' not in payload or 'task_name' not in payload:
            raise BodyParamsError("too less")

        # set up variables from event
        userId = payload['userId']
        task_name = payload['task_name']

        print({
            "userId": userId,
            "task_name": task_name
        }, "\n")

        recordList_table = dynamoDB_resource.Table(tableName)

        # query from table with conditions
        response = recordList_table.scan(
            FilterExpression=Key('userId').eq(userId) &
            Attr('task_name').eq(task_name)
        )

        print(response['Items'])

        result = 0
        for item in response['Items']:

            startTime_stamp = int(item['startTime'])

            endTime_stamp = int(item['endTime'])

            # Accumulate the focus time
            result += int((endTime_stamp-startTime_stamp)/(60*25))

        print(result)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "statusCode": 200,
                "body": result
            }, ensure_ascii=False)
        }

    except BodyParamsError as bpe:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "statusCode": 500,
                "body": bpe.message
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
