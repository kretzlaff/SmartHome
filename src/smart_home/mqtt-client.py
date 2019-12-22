import paho.mqtt.client as mqtt
import json


class MqttClient:

    def __init__(self):
        self.__client = mqtt.Client()
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.connect("192.168.50.135", 1883, 60)
        self.__client.loop_start()

    def __enter__(self):
        return self

    # ...

    def __exit__(self, exc_type, exc_value, traceback):
        self.__client.loop_stop()
        self.__client.disconnect()
        print("Disconnected")

    def publish(self, reciever, message):
        self.__client.publish("zigbee2mqtt/" + reciever + "/set", message)

    # The callback for when the client receives a CONNACK response from the server.

    def __on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        # client.subscribe("$SYS/#")

    # The callback for when a PUBLISH message is received from the server.

    def __on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
