import json
import boto3
from uuid import uuid4
from boto3.dynamodb.conditions import Key
from datetime import datetime

TABLE_NAME = 'team16_final_project_future_todoList'
dynamoDB_resource = boto3.resource('dynamodb')
scheduler_client = boto3.client('scheduler')

class BodyParamsError(Exception):
    # two types: "too less" or "too many" params
    def __init__(self, type):
        if type == 'too less':
            self.message = 'body params must have the following attributes: 1. "userId", 2. "timestamp" 3. "name"'

def lambda_handler(event, context):
    # see what pass in
    # print(json.dumps(event))
    
    try:
        # validate payload
        payload = json.loads(event['body'])
        if 'userId' not in payload or 'timestamp' not in payload or 'name' not in payload:
            raise BodyParamsError("too less")
        
        # TODO: too many params
    
        # initialize dynamoDB
        todoList_table = dynamoDB_resource.Table(TABLE_NAME)
        
        # set up uuid for eventbridge and dynamoDB
        scheduler_uuid = str(uuid4())
        
        # check the partition and sort key already existed
        response = todoList_table.query(
            KeyConditionExpression=
                Key('userId').eq(payload['userId']) &
                Key('todo_timestamp').eq(payload['timestamp'])
        )
        
        # if not existed, create an item
        if len(response['Items']) == 0:
            new_item = {
                'userId': payload['userId'],
                'todo_timestamp': payload['timestamp'],
                'todo_name': [payload['name']],
                'todo_description': [payload['description'] if 'description' in payload else None],
                'todo_finished': [False],
                'sns_uuid': [scheduler_uuid],
                'records_uuid': [None],
                'created_time': str(int(datetime.now().timestamp())),
                'updated_time': str(int(datetime.now().timestamp()))
            }
        # if already existed, and there should be only one item.
        # updated "todo_name", "todo_description", "updated_time" in the original item
        else:
            new_item = response['Items'][0]
            new_item['todo_name'].append(payload['name'])
            new_item['todo_description'].append(payload['description'] if 'description' in payload else None)
            new_item['todo_finished'].append(False),
            new_item['sns_uuid'].append(scheduler_uuid)
            new_item['records_uuid'].append(None),
            new_item['updated_time'] = str(int(datetime.now().timestamp()))
        
        todoList_table.put_item(Item=new_item)
            
        
        # create eventbridge on that specific time
        scheduler_datetime = datetime.fromtimestamp(int(payload['timestamp'])-5*60).strftime("%Y-%m-%dT%H:%M:%S")
        notification_string = '您於"{}"有預定要做「{}」事項，趕快透過番茄時鐘來紀錄吧!'.format(
            datetime.fromtimestamp(int(payload['timestamp'])+8*60*60).strftime("%H:%M"),
            payload['name']
        )
        
        scheduler_client.create_schedule(
            Name=scheduler_uuid,
            GroupName='team16_111065508_final_projects',
            FlexibleTimeWindow={'Mode': 'OFF'},
            ScheduleExpression='at({})'.format(scheduler_datetime),
            EndDate= datetime.fromtimestamp(int(payload['timestamp'])+5*60),
            Target={
                'Arn': 'arn:aws:sns:us-east-1:591886860315:team16_final-project-{}'.format(payload['userId']),
                'Input': notification_string,
                'RoleArn': 'arn:aws:iam::591886860315:role/service-role/team16_111065508_final-projects_eventbridge-scheduler_sns'
            }
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "statusCode": 200,
                "body": 'payload: "{}" insert successfully'.format(payload)
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
        
    except Exception as err:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "statusCode": 500,
                "body": str(err)
            })
        }