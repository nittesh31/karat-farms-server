# Import package
import paho.mqtt.client as mqtt
import ssl
import io
from PIL import Image, ImageShow
import logging
import boto3
from botocore.exceptions import ClientError # Define Variables
import datetime
import psycopg2

MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "video/+"

MQTT_HOST = "a3nov961lj6kjd-ats.iot.us-west-2.amazonaws.com"
CA_ROOT_CERT_FILE = "/Users/apple/karat-farms/karat-farms-server/saleor/iot/root-CA.crt"
THING_CERT_FILE = "/Users/apple/karat-farms/karat-farms-server/saleor/iot/auto-irrigate-test.cert.pem"
THING_PRIVATE_KEY = "/Users/apple/karat-farms/karat-farms-server/saleor/iot/auto-irrigate-test.private.key"

s3_client = boto3.client('s3',
                         aws_access_key_id='AKIAJMONY4HMYTLPXIWA',
                         aws_secret_access_key='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')

myConnection = psycopg2.connect(host='localhost', user='saleor', password='saleor', dbname='saleor')
print(myConnection)
cur = myConnection.cursor()

def writeToDB(email, imgName):
    x = cur.execute("INSERT INTO iot_farmimage (email, image_name, time_created) VALUES (%s, %s, %s)", (email, imgName, datetime.datetime.now()))
    myConnection.commit()

def byte_array_to_pil_image(byte_array):
    return Image.open(io.BytesIO(byte_array))

# Define on connect event function
# We shall subscribe to our Topic in this function
def on_connect(mosq, obj, flags, rc):
    print("connected")
    mqttc.subscribe(MQTT_TOPIC, 0)


# Define on_message event function.
# This function will be invoked every time,
# a new message arrives for the subscribed topic
def on_message(mosq, obj, msg):
    # print("Topic: " + str(msg.topic))
    # print("QoS: " + str(msg.qos))
    print("yeah")
    print("Topic :", str(msg.topic))
    # print("Payload: " + str(msg.payload))
    print("###################")
    # imageByteString = msg.payload
    # strings = imageByteString.split(',')
    # strings = [int(i) for i in strings]
    # for string in strings:
    #     print(string)

    # print(io.BytesIO(imageBytes))
    # img = Image.fromarray(msg.payload, 'RGB')

    user_email = str(msg.topic).split('/')[1]
    print(user_email)
    img = byte_array_to_pil_image(msg.payload)
    in_mem_file = io.BytesIO()
    img.save(in_mem_file, 'jpeg')
    in_mem_file.seek(0)
    imgName = user_email + "-" + str(datetime.datetime.now()) + ".jpg"
    s3_client.upload_fileobj(in_mem_file, "karat-video-test", imgName)
    print("uploaded")
    writeToDB(user_email, imgName)
    print("@@@@@@@")




def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed to Topic: " + MQTT_TOPIC + " with QoS: " + str(granted_qos))


# Initiate MQTT Client
mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Configure TLS Set
mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)


# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
# Continue monitoring the incoming messages for subscribed topic
mqttc.loop_forever()
