import boto3
import json
from boto3.dynamodb.conditions import Key
from datetime import datetime
from exception_utili import *

TABLE_NAME = 'team16_final_project_future_todoList'
dynamoDB_resource = boto3.resource('dynamodb')
scheduler_client = boto3.client('scheduler')
            
def lambda_handler(event, context):
    # print(json.dumps(event)) # see what pass in
    
    try:
        '''
        validate payload
        '''
        payload = json.loads(event['body'])
        if not validate_payload(payload):
            raise BodyParamsError('too less')
        
        if not validate_additional_payload(payload):
            raise BodyParamsError('too many')
        
        if not validate_addional_attribute(payload['attributes']):
            raise BodyParamsError('attributes error')
        
        
        '''
        initialize dynamoDB
        '''
        todoList_table = dynamoDB_resource.Table(TABLE_NAME) 
        
        
        ''' 
        find the target item 
        '''
        response = todoList_table.query(
            KeyConditionExpression=
                Key('userId').eq(payload['userId']) &
                Key('todo_timestamp').eq(payload['timestamp'])
        )
        
        '''
        if not existed, raise error
        '''
        if len(response['Items']) == 0:
            raise NoTargetItemError()
        
        new_item = response['Items'][0]
        target_index = new_item['todo_name'].index(payload['name']) # if find no todo name, it will raise ValueError
        
        scheduler_uuid = new_item['sns_uuid'][target_index]
        
        toChangeTimestamp = False
        timstamp_afterChange = ''
        
        '''
        update value with given attribute
        and check timestamp needs to change or not.
        if yes, note it
        '''
        for attr in payload['attributes']:
            if attr['type'] == 'todo_timestamp':
                toChangeTimestamp = True
                timstamp_afterChange = attr['content']
            else:
                new_item[attr['type']][target_index] = attr['content']

        
        '''
        If timestamp doesn't need to change, just update the original item;
        otherwise...
        
        First, we need to extract the item information, and do deletion on the original timestamp item.
        Next, check the new timestamp exists or not.
        If yes, append the information on it. 
        If not, insert a new item.
        '''
        if not toChangeTimestamp:
            todoList_table.put_item(Item=new_item)
        else:
            todo_name = new_item['todo_name'].pop(target_index)
            todo_description = new_item['todo_description'].pop(target_index)
            todo_status = new_item['todo_finished'].pop(target_index)
            todo_sns_uuid = new_item['sns_uuid'].pop(target_index)
            todo_records_uuid = new_item['records_uuid'].pop(target_index)
            
            '''
            Do deletion.
            If there is no todo at that time, just remove whole item;
            Otherwise, update the original timestamp item
            '''
            if len(new_item['todo_name']) == 0:
                todoList_table.delete_item(
                    Key={
                        'userId': payload['userId'],
                        'todo_timestamp': payload['timestamp']
                    }
                )
            else:
                todoList_table.put_item(Item=new_item)
            
            '''    
            Create or insert new todo into new timestamp.
            First, check it is already existed or not.
            If not, create it.
            If yes, append it.
            '''
            response = todoList_table.query(
                KeyConditionExpression=
                    Key('userId').eq(payload['userId']) &
                    Key('todo_timestamp').eq(timstamp_afterChange)
            )
            
            if len(response['Items']) == 0:  # it doesn't exist
                new_item={
                    'userId': payload['userId'],
                    'todo_timestamp': timstamp_afterChange,
                    'todo_name': [todo_name],
                    'todo_description': [todo_description],
                    'todo_finished': [todo_status],
                    'sns_uuid': [todo_sns_uuid],
                    'records_uuid': [todo_records_uuid],
                    'created_time': str(int(datetime.now().timestamp())),
                    'updated_time': str(int(datetime.now().timestamp()))
                }
            else:
                new_item = response['Items'][0]
                new_item['todo_name'].append(todo_name)
                new_item['todo_description'].append(todo_description)
                new_item['todo_finished'].append(todo_status)
                new_item['sns_uuid'].append(todo_sns_uuid)
                new_item['records_uuid'].append(todo_records_uuid)
                new_item['updated_time'] = str(int(datetime.now().timestamp()))
                
            todoList_table.put_item(Item=new_item)
        
        '''
        change todo in the past, so there is no need to change scheduler
        '''
        if int(new_item['todo_timestamp']) <= int(datetime.now().timestamp()):
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "statusCode": 200,
                    "body": 'payload: "{}" update successfully'.format(payload)
                })
            }
            
            
        '''
        update the scheduler eventbridge with new item
        '''
        scheduler_datetime = datetime.fromtimestamp(int(new_item['todo_timestamp'])-5*60).strftime("%Y-%m-%dT%H:%M:%S")
        notification_string = '您於"{}"有預定要做「{}」事項，趕快透過番茄時鐘來紀錄吧!'.format(
            datetime.fromtimestamp(int(new_item['todo_timestamp'])+8*60*60).strftime("%H:%M"),
            todo_name
        )
        
        scheduler_client.update_schedule(
            Name=scheduler_uuid,
            GroupName='team16_111065508_final_projects',
            FlexibleTimeWindow={'Mode': 'OFF'},
            ScheduleExpression='at({})'.format(scheduler_datetime),
            EndDate= datetime.fromtimestamp(int(new_item['todo_timestamp'])+5*60),
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
                "body": 'payload: "{}" update successfully'.format(payload)
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
    
    except NoTargetItemError as ntie:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "statusCode": 500,
                "body": ntie.message
            })
        }
    
    except ValueError as ve:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "statusCode": 500,
                "body": 'find no item with the given todoName'
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