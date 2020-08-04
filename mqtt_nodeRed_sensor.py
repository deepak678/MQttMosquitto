#environment setup install mosquitto in raspberry pi
#take subscriber mqtt node in node red and a debug node to see the messages
#importing mqtt and gpio for raspberry pi
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

#circuit setup sensor is attached to pin 16 and one extra bulb is 
#attached to 18 pin of raspberry pi
sensor = 16
led = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(led,GPIO.OUT)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

client = mqtt.Client()
client.on_connect = on_connect
#ip of raspberry pi
client.connect("192.168.43.245", 1883, 60)

#whenever an object is detected in front of an infrared sensor 
# one led bulb gets turned on and message gets published to /test topic
#that message is also displayed on node red debug node
try:
   while True:
      if GPIO.input(sensor):
          client.publish('/test',payload = 'Object Detected')
          GPIO.output(led, GPIO.HIGH)
          while GPIO.input(sensor):
              time.sleep(0.2)
      else:
        GPIO.output(led, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
