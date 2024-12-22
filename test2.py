import paho.mqtt.client as paho
import os
import socket
import ssl
from time import sleep
from random import uniform
import json
import subprocess
import signal
import logging
logging.basicConfig(level=logging.INFO)
global display_process

# Refactored original source - https://github.com/mariocannistra/python-paho-mqtt-for-aws-iot

class PubSub(object):

    def __init__(self, listener = False, topic = "default"):
        self.connect = False
        self.listener = listener
        self.topic = topic
        self.logger = logging.getLogger(repr(self))

    def __on_connect(self, client, userdata, flags, rc):
        self.connect = True
        
        if self.listener:
            self.mqttc.subscribe(self.topic)

        self.logger.debug("{0}".format(rc))

    def __on_message(self, client, userdata, msg):
        self.logger.info("{0}, {1} - {2}".format(userdata, msg.topic, msg.payload))
        msg_json = json.loads(msg.payload)
        if msg_json['message'] == "textScroll":
            try:
                kill = subprocess.Popen([f'sudo kill -9 {pid}'])
                display_process = subprocess.Popen([f'sudo /home/inigo/panel/rpi-rgb-led-matrix/examples-api-use/scrolling-text-example -f ../fonts/ibmfonts/bdf/ic8x16u.bdf --led-rows=64 --led-cols=64 --led-gpio-mapping=regular-pi1 {msg_json["content"]} -y {msg_json["y"]} -x {msg_json["x"]}'], shell=True)
            except UnboundLocalError:
                print("UnboundLocal")
                display_process = subprocess.Popen([f'sudo /home/inigo/panel/rpi-rgb-led-matrix/examples-api-use/scrolling-text-example -f ../fonts/ibmfonts/bdf/ic8x16u.bdf --led-rows=64 --led-cols=64 --led-gpio-mapping=regular-pi1 {msg_json["content"]} -y {msg_json["y"]} -x {msg_json["x"]}'], shell=True)

            global pid 
            pid = display_process.pid
        #os.system('sudo /home/inigo/panel/rpi-rgb-led-matrix/examples-api-use/minimal-example --led-cols=64 --led-rows=64 --led-gpio-mapping=regular-pi1')

    def __on_log(self, client, userdata, level, buf):
        self.logger.debug("{0}, {1}, {2}, {3}".format(client, userdata, level, buf))

    def bootstrap_mqtt(self):

        self.mqttc = paho.Client()
        self.mqttc.on_connect = self.__on_connect
        self.mqttc.on_message = self.__on_message
        self.mqttc.on_log = self.__on_log

        awshost = "a13g4qp9um7jpd-ats.iot.eu-north-1.amazonaws.com"
        awsport = 8883

        caPath = "./rootCA.pem" # Root certificate authority, comes from AWS with a long, long name
        certPath = "e516aeafcc243931eda22607263797bbb8c639cc00774ab0a9188150f3d1e2e1-certificate.pem.crt"
        keyPath = "e516aeafcc243931eda22607263797bbb8c639cc00774ab0a9188150f3d1e2e1-private.pem.key"

        self.mqttc.tls_set(caPath, 
            certfile=certPath, 
            keyfile=keyPath, 
            cert_reqs=ssl.CERT_REQUIRED, 
            tls_version=ssl.PROTOCOL_TLSv1_2, 
            ciphers=None)

        result_of_connection = self.mqttc.connect(awshost, awsport, keepalive=120)

        if result_of_connection == 0:
            self.connect = True

        return self

    def start(self):
        self.mqttc.loop_start()

        while True:
            sleep(2)
            if self.connect == True:
                #self.mqttc.publish(self.topic, json.dumps({"message": "Hello COMP680"}), qos=1)
                pass
            else:
                self.logger.debug("Attempting to connect.")

if __name__ == '__main__':
    
    PubSub(listener = True, topic = "chat-evets").bootstrap_mqtt().start()
