import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time

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

client.connect("192.168.43.245", 1883, 60)

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
