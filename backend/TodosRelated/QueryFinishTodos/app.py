import json
import boto3
from boto3.dynamodb.conditions import Key
import time
import datetime


dynamoDB_resource = boto3.resource('dynamodb')


class QueryFinishParamsError(Exception):
    def __init__(self):
        self.message = 'query params must have the following attributes: "userId"'


def lambda_handler(event, context):
    # see what pass in
    # return {
    #     "statusCode": 200,
    #     "body": json.dumps(event)
    # }

    try:
        # check query params first
        queryParams = event['queryStringParameters']
        if 'userId' not in queryParams:
            raise QueryFinishParamsError()

        # set up variables from event
        userId = queryParams['userId']

        # get the  timestamp for duration
        query_today = str(int(time.mktime(
            (datetime.date.today() + datetime.timedelta(days=1)).timetuple())))
        query_oneWeekAgo = str(int(time.mktime(
            (datetime.date.today() - datetime.timedelta(days=6)).timetuple())))

        # see variables
        print({
            "userId": userId,
            "query_oneWeekAgo": query_oneWeekAgo,
            "query_today": query_today
        }, "\n")

        # initialize todo list table
        tableName = 'team16_final_project_future_todoList'
        todoList_table = dynamoDB_resource.Table(tableName)

        # query from table with conditions
        response = todoList_table.query(
            KeyConditionExpression=Key('userId').eq(userId) &
            Key('todo_timestamp').between(query_oneWeekAgo, query_today)
        )

        # print(response['Items'])

        # reconstuct query response
        result_week = {}
        for i in range(0, 7):
            result_week[(datetime.date.today() -
                         datetime.timedelta(days=i)).strftime('%A')] = []

        print(result_week)

        result = []
        for item in response['Items']:
            for i in range(len(item['todo_name'])):
                # Check if todo whether finished or not
                if item['todo_finished'][i]:
                    # Turn the timestamp to weekday
                    time_stamp = int(item['todo_timestamp'])
                    struct_time = time.localtime(time_stamp)
                    week_day = time.strftime("%A", struct_time)

                    result_week[week_day].append({
                        'userId': item['userId'],
                        'timestamp': item['todo_timestamp'],
                        'name': item['todo_name'][i],
                        'description': item['todo_description'][i]
                    })

        # print(result_week)

        loaded = json.loads(json.dumps(result_week))
        result_count = {}
        for iterator in loaded:
            result_count[iterator] = len(result_week[iterator])

        # print(result_count)
        result = []
        # result.append(result_week)
        result.append(result_count)
        # print(result)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "statusCode": 200,
                "body": result
            }, ensure_ascii=False)
        }

    except QueryFinishParamsError as qe:
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
