import paho.mqtt.client as mqtt
    
root_CA_cert = '../thing_certificate/AmazonRootCA1.pem'
device_cert = '../thing_certificate/5ad02c58ca5f6a605abeb003491020f6bded9439f638d5d09bd558ae9d531197-certificate.pem.crt'
private_pem_key = '../thing_certificate/5ad02c58ca5f6a605abeb003491020f6bded9439f638d5d09bd558ae9d531197-private.pem.key'
iot_endpoint = 'a1io7cze9x1oli-ats.iot.us-east-1.amazonaws.com'


class MQTT:
    def __init__(self, topicArray) -> None:
        self.__mqttc = mqtt.Client(protocol=mqtt.MQTTv5)  
        self.topic_array = topicArray
        
        self.received_message = None
        
    def bootstrap_mqtt(self):   
        self.__mqttc.tls_set(
            ca_certs=root_CA_cert,
            certfile=device_cert,
            keyfile=private_pem_key,
            tls_version=2
        )
        self.__mqttc.on_connect = self.__on_connect
        self.__mqttc.on_message = self.__on_message
        self.__mqttc.on_publish = self.__on_publish
        
        self.__mqttc.connect(iot_endpoint, 8883, 60)
        
    def __on_connect(self, client, userdata, flags, rc, properties=None):
        print(f"connected to endpoint {iot_endpoint} with result code {rc}")
        
        self.__mqttc.subscribe(self.topic_array)
        for topicName, Qos in self.topic_array:
            print(f"subscribed to topic {topicName}")
        
    def __on_message(self, client, userdata, msg):
        self.received_message = msg.payload.decode()
        # print(f"received message: topic: {msg.topic} payload: {msg.payload.decode()}")
    
    def __on_publish(self, client, userdata, mid):
        print("message sent successfully")
    
    def is_connected(self):
        return self.__mqttc.is_connected()
    
    def loop_start(self):
        self.__mqttc.loop_start()
        
    def publish(self, topic, payload):
        self.__mqttc.publish(topic, payload)