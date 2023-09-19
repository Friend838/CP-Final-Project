import boto3
import json
import sys
import time

##########################################################
# Connect to SQS and poll for messages
##########################################################
rekognition_client = boto3.client('rekognition')

QUEUE_NAME = 'team16_finalproject'
sqs_resource = boto3.resource('sqs')
output_queue = sqs_resource.get_queue_by_name(QueueName=QUEUE_NAME)

iotClient = boto3.client('iot-data')

def lambda_handler(event, context):
	print(json.dumps(event))
	
	bucketName = event['Records'][0]['s3']['bucket']['name']
	key = event['Records'][0]['s3']['object']['key']
 
	_, userId, _ = key.split('/')

	# Inference image
	has_person = inference_image(bucketName, key)
	print("has person: ", has_person)	
 
	if has_person:
		payload = json.dumps({
			"userId": userId,
			"has_person": True
		})
  
		iotClient.publish(
			topic='team16/pi',
			payload=json.dumps({
				"userId": userId,
				"action": "light on"
			})
		)
	else:
		payload = json.dumps({
			"userId": userId,
			"has_person": False
		})
  
		iotClient.publish(
			topic='team16/pi',
			payload=json.dumps({
				"userId": userId,
				"action": "light off"
			})
		)

	print("payload: ", payload)
	output_queue.send_message(MessageBody=payload)
	
	return

def inference_image(bucketName, key):
	try:
		result = rekognition_client.detect_labels(
			Image = {
				"S3Object": {
					"Bucket": bucketName,
					"Name": key
				}
			}
		)

		labels = result['Labels']
		
		for object in labels:
			if object['Name'] == 'Person':
				return True
		else:
			return False
  
	except Exception as e:
		print(e)
		print(sys.exc_info()[0])