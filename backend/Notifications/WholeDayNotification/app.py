import boto3
import traceback

from uuid import uuid4
from boto3.dynamodb.conditions import Key
from datetime import datetime
from dateutil import tz

dynamo_resource = boto3.resource('dynamodb')
todo_table = dynamo_resource.Table('team16_final_project_future_todoList')
day_sns_table = dynamo_resource.Table('team16_finalProject_day_notifications')

schdeuler_client = boto3.client('scheduler')

USERID = '8787878787'

def lambda_handler(event, context):
    try:
        datetime_now = datetime.now(tz.gettz('Asia/Taipei'))
        target_date = datetime(datetime_now.year, datetime_now.month, datetime_now.day+1).strftime("%Y-%m-%d")
        start_timestamp = str(int(datetime(datetime_now.year, datetime_now.month, datetime_now.day+1).timestamp()))
        end_timestamp = str(int(datetime(datetime_now.year, datetime_now.month, datetime_now.day+2).timestamp())-1)
        
        todos_in_range = todo_table.query(
            KeyConditionExpression=Key('userId').eq(USERID) & 
                                Key('todo_timestamp').between(start_timestamp, end_timestamp)
        )['Items']
        
        if len(todos_in_range) == 0:
            print("no any todos tomorrow")
            return
        
        scheduler_uuid = str(uuid4())
        scheduler_datetime = datetime(datetime_now.year, datetime_now.month, datetime_now.day, 23, 30) \
                                .replace(tzinfo=tz.gettz('Asia/Taipei')) \
                                .strftime("%Y-%m-%dT%H:%M:%S")
        notification_message = f'您於明日 "{target_date}" 有預訂以下事情:\n'
        index = 1
        for todos in todos_in_range:
            todo_time = datetime.fromtimestamp(int(todos['todo_timestamp']), tz=tz.gettz('Asia/Taipei')).strftime('%H:%M')
            for todo in todos['todo_name']:
                notification_message += f'{index}. "{todo_time}"  "{todo}"\n'
                index += 1
        
        print(notification_message)
        
        schdeuler_client.create_schedule(
            Name=scheduler_uuid,
            GroupName='team16_111065508_final_projects',
            FlexibleTimeWindow={'Mode': 'OFF'},
            ScheduleExpression='at({})'.format(scheduler_datetime),
            ScheduleExpressionTimezone='Asia/Taipei',
            EndDate= datetime.fromtimestamp(int(start_timestamp)),
            State='ENABLED',
            Target={
                'Arn': 'arn:aws:sns:us-east-1:591886860315:team16_final-project-{}'.format(USERID),
                'Input': notification_message,
                'RoleArn': 'arn:aws:iam::591886860315:role/service-role/team16_111065508_final-projects_eventbridge-scheduler_sns'
            }
        )
        
        day_sns_table.put_item(
            Item = {
                'sns_target_date': target_date,
                'scheduler_uuid': scheduler_uuid,
                'created_time': str(int(datetime.utcnow().timestamp())),
                'updated_time': str(int(datetime.utcnow().timestamp()))
            }
        )
        
        return
    
    except:
        print(traceback.format_exc())
        
        return