import sys
import time
import json
import signal
import RPi.GPIO as GPIO

from pygame import mixer
from MQTT_utili import MQTT

BREAK_SOUND_PATH = "./break.mp3"
mixer.init()

GPIO.setmode(GPIO.BOARD)
led = 18
GPIO.setup(led, GPIO.OUT)

def play_sound(sound_file):
    mixer.music.load(sound_file)
    mixer.music.play()
    while mixer.music.get_busy() == True:
        time.sleep(0.1)

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    GPIO.cleanup()
    sys.exit(0)       

if __name__ == "__main__":
    mqttc = MQTT([('team16/pi', 0)])
    mqttc.bootstrap_mqtt()
    mqttc.loop_start()
    
    last_message = None
    while 1:
        signal.signal(signal.SIGINT, signal_handler)
        
        if mqttc.received_message != last_message:
            print("received message: ", mqttc.received_message)
            last_message = mqttc.received_message
            
            action = json.loads(mqttc.received_message)['action']
            if action == 'break':
                play_sound(BREAK_SOUND_PATH)
            elif action == 'light on':
                GPIO.output(led, GPIO.HIGH)
            elif action == 'light off':
                GPIO.output(led, GPIO.LOW)

        time.sleep(1)