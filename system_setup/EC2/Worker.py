import threading
import time
import json
import boto3

from datetime import datetime
from MQTT_utili import MQTT

fast = True

STATE_TABLE = {
    0: 'sleeping',
    1: 'cold_start',
    2: 'working',
    3: 'awaiting',
    4: 'break'
}

def coldStart2working(event: threading.Event):
    if fast:
        event.wait(30)
    else:
        event.wait(5*60)
    
def working2break(event: threading.Event):
    '''
    Problem:
    如果只是變成await，還是會繼續計時。
    如果要改成可以暫停計時，然後繼續計時，需要重想方案。
    '''
    if fast:
        event.wait(1*60)
    else:
        event.wait(25*60)
    if event.is_set():
        return
    
def awaiting2sleeping(event: threading.Event):    
    if fast:
        event.wait(40)
    else:
        event.wait(3*60)
    if event.is_set():
        return
    
def break2sleeping(event: threading.Event):
    if fast:
        event.wait(1*60)
    else:
        event.wait(5*60)
        
class Worker():
    def __init__(self, name):
        print("init worker {}".format(name))
        
        self.name = name
        self.passive = True 
        self.proactive = False
        self.stopped = False
        
        self.__rekoResult = None
        
        self.__state = STATE_TABLE[0]
        self.startTimestamp = 0
        self.endTimestamp = 0
        self.taskName = None
        
        # self.__dynamo_resource = boto3.resource('dynamodb')
        self.__dynamo_resource = boto3.Session(profile_name='CP_team16').resource('dynamodb')
        
        
        topicArray = [('team16/fp', 0)]
        self.__mqttClient = MQTT(topicArray)
        self.__mqttClient.bootstrap_mqtt()
        self.__mqttClient.loop_start()
        
        self.__coldStartInterrupt = threading.Event()        
        self.__coldStartThread = None
        
        self.__workingInterrupt = threading.Event()
        self.__workingThread = None
        
        self.__awaitingInterrupt = threading.Event()
        self.__awaitingThread = None
        
        self.__breakInterrupt = threading.Event()
        self.__breakThread = None

        print("worker {} init complete".format(name))
    
    def run(self):
        while not self.stopped:
            if self.__rekoResult == None:
                continue
            
            if self.get_state() == STATE_TABLE[0]:
                self.proactive = False
                self.passive = True
                self.reset_variable()
            
            if self.__mqttClient.received_message != None:
                message = json.loads(self.__mqttClient.received_message)
                print(message)

                if message['userId'] == self.name:
                    if message['action'] == 'manual_activate':
                        print("user {} has activate by manual".format(self.name))
                        self.proactive = True
                        self.passive = False
                        self.taskName = message['name']
                        
                        self.__coldStartInterrupt.set()
                        self.__workingInterrupt.set()
                        self.__awaitingInterrupt.set()
                        self.__breakInterrupt.set()
                        self.reset_variable()
                        self.change_state(STATE_TABLE[0])
                        
                    elif message['action'] == 'assign_task_name':
                        print("user {} has assign task name".format(self.name))
                        self.taskName = message['taskName']
                        
                        if self.endTimestamp == 0:
                            print(f"user {self.name} has assign task name, but this record doesn't take count")
                        elif self.endTimestamp != 0 and self.endTimestamp > self.startTimestamp:
                            print("record ready to push to DB")
                            self.push_record()  
                                            
                    self.__mqttClient.received_message = None
            
            if self.__rekoResult['has_person'] == True:
                if self.get_state() == STATE_TABLE[0]:
                    self.startTimestamp = int(datetime.now().timestamp())
                    
                    print("cold start started")
                    print("start working")
                    self.change_state(STATE_TABLE[1])
                    
                    self.__mqttClient.publish(
                        'team16/phone',
                        json.dumps({
                            "action": "start_record"
                        })
                    )
                    
                    self.__startColdStartThread()
                    self.__startWorkingThread()             
                
                elif self.get_state() == STATE_TABLE[1]:
                    if self.__coldStartThread.is_alive() == False:
                        self.__coldStartThread.join()
                        print("cold start ended")
                        self.change_state(STATE_TABLE[2])
                        
                elif self.get_state() == STATE_TABLE[2]:
                    if self.__workingThread.is_alive() == False:
                        self.__workingThread.join()
                        print("work full 25 mins, take a break")

                        self.endTimestamp = int(datetime.now().timestamp())
                        
                        # TODO: push to dynamoDB
                        print("record ended")   
                          
                        self.__mqttClient.publish(
                            'team16/pi',
                            json.dumps({
                                "userId": self.name,
                                "action": "break"
                            })
                        )
                        
                        self.__mqttClient.publish(
                            'team16/phone',
                            json.dumps({
                                "action": "end_record"
                            })
                        )
                        
                        self.change_state(STATE_TABLE[4])
                        self.__startBreakThread()
                
                elif self.get_state() == STATE_TABLE[3]:
                    if self.__awaitingThread.is_alive() == True:
                        self.__awaitingInterrupt.set()
                        time.sleep(0.1) 
                        self.__awaitingThread.join()
                        
                        if self.__workingThread.is_alive():
                            print("person comes back, continue working")
                            self.change_state(STATE_TABLE[2])
                        else:
                            print("person comes back, but work is already finished")
                            self.__workingThread.join()
                            
                            print("record ended") 
                            
                            self.__mqttClient.publish(
                                'team16/pi',
                                json.dumps({
                                    "userId": self.name,
                                    "action": "break"
                                })
                            )
                            
                            self.__mqttClient.publish(
                                'team16/phone',
                                json.dumps({
                                    "action": "end_record"
                                })
                            )
                        
                            self.change_state(STATE_TABLE[4])
                            self.__startBreakThread()
                
                elif self.get_state() == STATE_TABLE[4]:
                    if self.__breakThread.is_alive() == False:
                        self.__breakThread.join()
                        print("break ended")
                        self.change_state(STATE_TABLE[0])
                        
            else:
                if self.get_state() == STATE_TABLE[1]:
                    if self.__coldStartThread.is_alive() == True:
                        print("person has gone, and cold start is still going, not recording")
                        self.__mqttClient.publish(
                            'team16/phone',
                            json.dumps({
                                "action": "end_record"
                            })
                        )
                        
                        self.change_state(STATE_TABLE[0])
                        self.__coldStartInterrupt.set()
                        self.__workingInterrupt.set()
                        time.sleep(0.1)
                        self.__coldStartThread.join()
                        self.__workingThread.join()
                
                elif self.get_state() == STATE_TABLE[2]:
                    if self.__workingThread.is_alive() == True:
                        print("person has gone, start awaiting")
                        
                        self.endTimestamp = int(datetime.now().timestamp())
                        
                        self.change_state(STATE_TABLE[3])
                        # self.__workingInterrupt.set()
                        # time.sleep(0.1)
                        self.__startAwaitingThread()
                
                elif self.get_state() == STATE_TABLE[3]:
                    if self.__awaitingThread.is_alive() == False:
                        self.__awaitingThread.join()
                        print("person doesn't comeback, stop recording")
                        
                        print("record ended")
                        
                        self.__mqttClient.publish(
                            'team16/phone',
                            json.dumps({
                                "action": "end_record"
                            })
                        )
                        
                        self.change_state(STATE_TABLE[0])
                        self.__workingInterrupt.set()
                        time.sleep(0.1)
                        self.__workingThread.join()
                
                elif self.get_state() == STATE_TABLE[4]:
                    if self.__breakThread.is_alive() == False:
                        self.__breakThread.join()
                        print("break ended")
                        self.change_state(STATE_TABLE[0])
    
    def __startColdStartThread(self):
        self.__coldStartThread = threading.Thread(target=coldStart2working, args=(self.__coldStartInterrupt,))
        self.__coldStartThread.start()
    
    def __startWorkingThread(self):
        self.__workingThread = threading.Thread(target=working2break, args=(self.__workingInterrupt,))
        self.__workingThread.start()
    
    def __startAwaitingThread(self):
        self.__awaitingThread = threading.Thread(target=awaiting2sleeping, args=(self.__awaitingInterrupt,))
        self.__awaitingThread.start()
        
    def __startBreakThread(self):
        self.__breakThread = threading.Thread(target=break2sleeping, args=(self.__breakInterrupt,))
        self.__breakThread.start()
    
    def get_state(self):
        return self.__state
    
    def reset_variable(self):
        self.startTimestamp = 0
        self.endTimestamp = 0

        self.__coldStartInterrupt.clear()
        self.__coldStartThread = None
        self.__workingInterrupt.clear()
        self.__workingThread = None
        self.__awaitingInterrupt.clear()
        self.__awaitingThread = None
        self.__breakInterrupt.clear()
        self.__breakThread = None
    
    def change_state(self, targetState):
        print(f"State Change: {self.__state} -> {targetState}")
        self.__state = targetState
        
    def receive_rekoResult(self, message):
        print("receive result: {}".format(message))
        self.__rekoResult = message
    
    def push_record(self):
        table = self.__dynamo_resource.Table('team16_final_project_history_record')
        table.put_item(
            Item={
                "userId": self.name,
                "startTime": str(self.startTimestamp),
                "endTime": str(self.endTimestamp),
                "task_name": self.taskName,
                "created_time": str(int(datetime.utcnow().timestamp())),
                "updated_time": None,
                "deleted_time": None,
            }
        )
    
    def stop(self):
        self.stopped = True
        
        self.__coldStartInterrupt.set()
        self.__awaitingInterrupt.set()
        self.__workingInterrupt.set()
        self.__breakInterrupt.set()
        
        if self.__coldStartThread != None:
            self.__coldStartThread.join()
        if self.__workingThread != None:
            self.__workingThread.join()
        if self.__awaitingThread != None:
            self.__awaitingThread.join()
        if self.__breakThread != None:
            self.__breakThread.join()