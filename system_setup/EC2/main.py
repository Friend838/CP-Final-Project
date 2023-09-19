from Master import Master
import signal
import sys
import boto3

sqsURL = 'https://sqs.us-east-1.amazonaws.com/591886860315/team16_finalproject'


def signal_handler(signum, frame):
    print('You pressed Ctrl+C!')
    if signum == signal.SIGINT.value:
        master.purgeSQSMessage()
        master.stopAllWorkers()
        sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    master = Master(sqsURL)
    
    print("master start pulling from sqs")
    while 1:
        master.pull_message_from_sqs()
    