from Master import Master
import threading
import boto3

def input_message(queue_url):
    queue = boto3.Session(profile_name='CP_team16').resource('sqs').Queue(queue_url)
    while 1:
        message = input("input something: ")
        queue.send_message(MessageBody=message)

if __name__ == '__main__':
    queue_url = 'https://sqs.us-east-1.amazonaws.com/591886860315/team16_finalproject'
    master = Master(queue_url)
    
    print("sqs start pull")
    pull_thread = threading.Thread(target=master.pull_message_from_sqs)
    
    post_thread = threading.Thread(target=input_message, args=(queue_url,))
    
    pull_thread.start()
    
    post_thread.start()