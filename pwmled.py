import math
import RPi.GPIO as GPIO


class LED:
  def __init__(self):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # 11 = rouge
    # 13 = vert
    # 15 = bleu
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)

    self.r = GPIO.PWM(11, 80)  # channel=11 frequency=100Hz
    self.g = GPIO.PWM(13, 80)  # channel=13 frequency=100Hz
    self.b = GPIO.PWM(15, 80)  # channel=15 frequency=100Hz
    self.r.start(0)
    self.g.start(0)
    self.b.start(0)
    self.smooth = 20

  def calcLog(self,v):
  #	return v
	return 100-math.floor(100*(math.log(101+self.smooth-v)-math.log(self.smooth))/(math.log(101+self.smooth)-math.log(self.smooth)))

  def setRed(self,v):
	if v>=0 and v<=100: self.r.ChangeDutyCycle(self.calcLog(v))
  def setGreen(self,v):
	if v>=0 and v<=100: self.g.ChangeDutyCycle(self.calcLog(v))
  def setBlue(self,v):
	if v>=0 and v<=100: self.b.ChangeDutyCycle(self.calcLog(v))

  def stop(self):
    self.r.stop()
    self.g.stop()
    self.b.stop()
    GPIO.cleanup()

