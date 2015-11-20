#!/usr/bin/python
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)

p = GPIO.PWM(15, 100)  # channel=12 frequency=100Hz
p.start(0)
try:
    while 1:
        for dc in range(0, 101, 1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.01)
        for dc in range(100, -1, -1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.01)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()

