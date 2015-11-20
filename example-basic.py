#!/usr/bin/python
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)
while 1:
	GPIO.output(12,1)
	#GPIO.PWM(12,50)
	GPIO.output(12,0)
