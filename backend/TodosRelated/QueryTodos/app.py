import json
import boto3
from boto3.dynamodb.conditions import Key


dynamoDB_resource = boto3.resource('dynamodb')

class QueryParamsError(Exception):
    def __init__(self):
        self.message = 'query params must have the following attributes: 1. "userId", 2. "start_timestamp" 3. "end_timestamp"'
        
def lambda_handler(event, context):
    # see what pass in
    # return {
    #     "statusCode": 200,
    #     "body": json.dumps(event)
    # }
    
    try:
        
        # check query params first
        queryParams = event['queryStringParameters']
        if 'userId' not in queryParams or 'start_timestamp' not in queryParams or 'end_timestamp' not in queryParams:
            raise QueryParamsError()
        
        # set up variables from event
        userId = queryParams['userId']
        query_starttime = queryParams['start_timestamp']
        query_endtime = queryParams['end_timestamp']
        
        # see variables
        print({
            "userId": userId,
            "start_timestamp": query_starttime,
            "end_timestamp": query_endtime
        }, "\n")

        # initialize todo list table
        tableName = 'team16_final_project_future_todoList'
        todoList_table = dynamoDB_resource.Table(tableName)

        # query from table with conditions
        response = todoList_table.query(
            KeyConditionExpression=
                Key('userId').eq(userId) & 
                Key('todo_timestamp').between(query_starttime, query_endtime)
        )
        print(f"user {userId}'s all todos: ")
        print(response['Items'])
        print()
        
        # reconstuct query response
        result = []
        for item in response['Items']:
            for i in range(len(item['todo_name'])):
                result.append({
                    'userId': item['userId'],
                    'timestamp': item['todo_timestamp'],
                    'name': item['todo_name'][i],
                    'description': item['todo_description'][i],
                    'finishStatus': item['todo_finished'][i]
                })
        
        # change to record table
        tableName = 'team16_final_project_history_record'
        record_table = dynamoDB_resource.Table(tableName)
        
        # scan all record items first
        response = record_table.scan(
            FilterExpression=Key('userId').eq(userId)
        )
        print(f"user {userId}'s all records: ")
        print(response['Items'])
        
        # count "tomato clock" to each todo name
        for i in range(len(result)):
            todoName = result[i]['name']
            tomatoCount = count_tomato(response['Items'], todoName)
            result[i]['tomatoCount'] = tomatoCount
            
        return {
            "statusCode": 200,
            "body": json.dumps({
                "statusCode": 200,
                "body": result   
            }, ensure_ascii=False)
        }
        
    except QueryParamsError as qe:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "statusCode": 500,
                "body": qe.message
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
        
        
def count_tomato(data, taskName):
    print("task name: ", taskName)
    records_for_a_task = [item for item in data if item['task_name'] == taskName]
    # records_for_a_task = list(filter(lambda x: x['task_name'] == taskName, data))
    print(records_for_a_task)
    
    total_seconds = 0
    for item in records_for_a_task:
        total_seconds += int(item['endTime']) - int(item['startTime'])
    print(total_seconds)
    
    return total_seconds // (25*60)