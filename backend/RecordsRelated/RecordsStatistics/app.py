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
        tableName = 'team16_final_project_history_record'
        recordList_table = dynamoDB_resource.Table(tableName)

        # query from table with conditions
        response = recordList_table.query(
            KeyConditionExpression=Key('userId').eq(userId) &
            Key('startTime').between(query_oneWeekAgo, query_today)
        )

        # print(response['Items'])

        # reconstuct query response
        result_week = {}
        for i in range(0, 7):
            result_week[(datetime.date.today() -
                         datetime.timedelta(days=i)).strftime('%A')] = 0

        # print(result_week)

        result = []
        for item in response['Items']:

            # Turn the timestamp to weekday
            startTime_stamp = int(item['startTime'])
            struct_time = time.localtime(startTime_stamp)
            week_day = time.strftime("%A", struct_time)

            endTime_stamp = int(item['endTime'])

            # Accumulate the focus time
            result_week[week_day] += (endTime_stamp-startTime_stamp)

        # print(result_week)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "statusCode": 200,
                "body": result_week
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
