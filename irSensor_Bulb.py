import RPi.GPIO as GPIO
import time

sensor = 16
led = 18

GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(led,GPIO.OUT)

try:
   while True:
      if GPIO.input(sensor):
          GPIO.output(led, GPIO.HIGH)
          while GPIO.input(sensor):
              time.sleep(0.2)
      else:
	GPIO.output(led, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()

