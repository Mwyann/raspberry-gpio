#!/usr/bin/python
import time
import math
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
# 11 = rouge
# 13 = vert
# 15 = bleu
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)

r = GPIO.PWM(11, 100)  # channel=11 frequency=100Hz
g = GPIO.PWM(13, 100)  # channel=13 frequency=100Hz
b = GPIO.PWM(15, 100)  # channel=15 frequency=100Hz
r.start(0)
g.start(0)
b.start(0)
smooth = 20

def calcLog(v):
#	return v
	return 100-math.floor(100*(math.log(101+smooth-v)-math.log(smooth))/(math.log(101+smooth)-math.log(smooth)))

def setRed(v):
	r.ChangeDutyCycle(calcLog(v))
def setGreen(v):
	g.ChangeDutyCycle(calcLog(v))
def setBlue(v):
	b.ChangeDutyCycle(calcLog(v))


try:
    while 1:
        for dc in range(0, 101, 1):
            setRed(dc)
            setGreen(dc)
            setBlue(dc)
            time.sleep(0.1)
        for dc in range(100, -1, -1):
            setRed(dc)
            setGreen(dc)
            setBlue(dc)
            time.sleep(0.1)
except KeyboardInterrupt:
    pass
r.stop()
g.stop()
b.stop()
GPIO.cleanup()

