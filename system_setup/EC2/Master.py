import ast
import boto3
import json

from threading import Thread
from multiprocessing import Process
from Worker import Worker
from MQTT_utili import MQTT

class Master:
    def __init__(self, sqsURL):
        self.sqs_queue = boto3.Session(profile_name='CP_team16').resource('sqs').Queue(sqsURL)
        # self.sqs_queue = boto3.resource('sqs').Queue(sqsURL)
        
        '''
        由worker自己跟MQTT連接
        '''
        # topicArray = [('team16/fp', 0)]
        # self.mqttc = MQTT(topicArray)
        
        self.worker_list = []
        self.thread_list = []
        
        self.worker_list.append(Worker('8787878787'))
        
        for worker in self.worker_list:
            thread = Thread(target=worker.run)
            self.thread_list.append(thread)
            thread.daemon = True
            thread.start()
            print("worker {} activates".format(worker.name))
        
        print(self.thread_list)
        
    def pull_message_from_sqs(self):
        response = self.sqs_queue.receive_messages(MaxNumberOfMessages=1)
        
        if len(response) != 0:
            for message in response:
                print(message.body)
                print(type(message.body))
                payload = json.loads(message.body)
                # payload = ast.literal_eval(message.body)
                message.delete()
            
            for worker in self.worker_list:
                if worker.name == payload['userId']:
                    worker.receive_rekoResult(payload)
                        
    def stopAllWorkers(self):
        for index, worker in enumerate(self.worker_list):
            worker.stop()
            print("worker {} stops".format(worker.name))
            self.thread_list[index].join()
            
    def purgeSQSMessage(self):
        self.sqs_queue.purge()