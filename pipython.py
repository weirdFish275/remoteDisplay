import time
import paho.mqtt.client as mqtt
import ssl
import json
import thread

import paho.mqtt.subscribe as subscribe

msg = subscribe.simple("paho/test/topic", hostname="a13g4qp9um7jpd-ats.iot.eu-north-1-amazonaws.com")
print("%s %s" % (msg.topic, msg.payload))

#client = mqtt.Client()
#client.on_connect = on_connect
#client.tls_set(ca_certs='./rootCA.pem', certfile='e516aeafcc243931eda22607263797bbb8c639cc00774ab0a9188150f3d1e2e1-certificate.pem.crt', keyfile='e516aeafcc243931eda22607263797bbb8c639cc00774ab0a9188150f3d1e2e1-private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
#client.tls_insecure_set(True)
#client.on_message = on_message
#client.on_subscribe = on_subscribe
#client.on_unsubscribe = on_unsubscribe
#client.user_data_set([])
#client.connect("a13g4qp9um7jpd-ats.iot.eu-north-1.amazonaws.com", 8883, 60) #Taken from REST API endpoint - Use your own. 


#client.loop_forever()
#print(f"Received the following message: {client.user_data_get()}")
