import json
import time
from MQTT_utili import MQTT

if __name__ == '__main__':
    topic_array = [('team16/fp', 1)]
    mqtt = MQTT(topic_array)
    mqtt.bootstrap_mqtt()
    mqtt.loop_start()
    
    while not mqtt.is_connected():
        time.sleep(1)
    
    mqtt.publish(
        'team16/fp', 
        json.dumps({
            "message": "hello from end device"
        })
    )
    
    while 1:
        time.sleep(1)