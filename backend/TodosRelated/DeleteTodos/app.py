import json
import boto3
from boto3.dynamodb.conditions import Key

TABLE_NAME = 'team16_final_project_future_todoList'
dynamoDB_resource = boto3.resource('dynamodb')
scheduler_client = boto3.client('scheduler')

class BodyParamsError(Exception):
    # two types: "too less" or "too many" params
    def __init__(self, type):
        if type == 'too less':
            self.message = 'body params must have the following attributes: 1. "userId", 2. "timestamp" 3. "name"'

class NoTargetItemError(Exception):
    def __init__(self):
        self.message = 'Find no item with the given userId and timestamp'
    
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
        
        # find the target item
        response = todoList_table.query(
            KeyConditionExpression=
                Key('userId').eq(payload['userId']) &
                Key('todo_timestamp').eq(payload['timestamp'])
        )
        
        # if not existed, raise error
        if len(response['Items']) == 0:
            raise NoTargetItemError()
        
        new_item = response['Items'][0]
        
        # if find no name, it will raise ValueError
        target_index = new_item['todo_name'].index(payload['name'])
        
        # find scheduler uuid for later eventbridge deletion 
        scheduler_uuid = new_item['sns_uuid'][target_index]
        
        # remove element on that index in these attributes: 
        # 1. todo_name
        # 2. todo_description
        # 3. todo_finished
        # 4. sns_uuid
        # 5. records_uuid
        new_item['todo_name'].pop(target_index)
        new_item['todo_description'].pop(target_index)
        new_item['todo_finished'].pop(target_index)
        new_item['sns_uuid'].pop(target_index)
        new_item['records_uuid'].pop(target_index)
        
        # after deletion, if there is no todo at that time, just remove whole item
        if len(new_item['todo_name']) == 0:
            todoList_table.delete_item(
                Key={
                    'userId': payload['userId'],
                    'todo_timestamp': payload['timestamp']
                }
            )
        # otherwise, update the original item
        else:
            todoList_table.put_item(Item=new_item)
            
        # delete target eventbridge
        scheduler_client.delete_schedule(
            Name=scheduler_uuid,
            GroupName='team16_111065508_final_projects'
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "statusCode": 200,
                "body": 'payload: "{}" delete successfully'.format(payload)
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