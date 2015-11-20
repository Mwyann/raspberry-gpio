import sys
import signal
import numpy
from recorder import *
from pwmled import *
import math

class Listen:

  def __init__(self,SR,led):  ## Constructeur
    self.SR = SR
    self.led = led
    self.Terminated = False
    self.sbcounter = -50
    self.sbskip = 0

  def standby(self):
    if (self.sbcounter < 0):
      self.sbcounter = self.sbcounter+1
      led.setRed(0)
      led.setGreen(0)
      led.setBlue(0)
      return 0
    else:
      self.sbskip = self.sbskip-1
      if (self.sbskip >= 0): return 0
      self.sbskip = 2
    
    self.sbcounter = self.sbcounter+1
    red = 0
    green = 0
    blue = 0
    if (self.sbcounter < 200): red = 100-math.fabs(100-self.sbcounter)
    
    if (self.sbcounter > 150): green = 100-math.fabs(250-self.sbcounter)
    
    if (self.sbcounter > 300): red = 100-math.fabs(400-self.sbcounter)
    if (self.sbcounter > 325): green = 100-math.fabs(400-self.sbcounter)
    
    if (self.sbcounter > 450): blue = 100-math.fabs(550-self.sbcounter)
    
    if (self.sbcounter > 600): red = 100-math.fabs(700-self.sbcounter)
    if (self.sbcounter > 625): blue = 100-math.fabs(700-self.sbcounter)
    
    if (self.sbcounter > 750): green = 100-math.fabs(850-self.sbcounter)
    if (self.sbcounter > 775):
      red = 100-math.fabs(850-self.sbcounter)
      blue = red
    
    if (self.sbcounter > 900):
      green = 100-math.fabs(950-self.sbcounter)
      blue = green
    
    if (self.sbcounter > 1000): red = 100-math.fabs(1100-self.sbcounter)
    
    if (self.sbcounter >= 1100): self.sbcounter = 100

    if (red < 0): red = 0
    if (green < 0): green = 0
    if (blue < 0): blue = 0
    led.setRed(red)
    led.setGreen(green)
    led.setBlue(blue)

  def loop(self):
    prevbass = 0
    prevmedium = 0
    prevtreble = 0
    agc = 0
    while not self.Terminated:
      if self.SR.newAudio!=False:
        xs,ys=self.SR.fft()
        bass=0
        medium=0
        treble=0
        for(i,freq) in enumerate(xs):
          if (freq < 400):
            bass+=ys[i]
          else:
            if (freq < 1200):
              medium+=ys[i]
            else:
              treble+=ys[i]
        print bass,' ; ',medium,' ; ',treble
        maxband = 500000
        if bass > maxband: maxband = bass
        if medium > maxband: maxband = medium
        if treble > maxband: maxband = treble
        if (maxband > agc): agc = maxband
        maxband = agc
        agc = agc*0.95
        reason = 'X'
        coeffbass = 0
        coeffmedium = 0
        coefftreble = 0
        if (prevbass > 0): coeffbass = bass/prevbass
        if (prevmedium > 0): coeffmedium = medium/prevmedium
        if (prevtreble > 0): coefftreble = treble/prevtreble
        if ((coeffbass > 1.1) or (coeffmedium > 1.2) or (coefftreble > 1.3)):
          coeff = coeffbass
          if (coeff < coeffmedium): coeff = coeffmedium
          if (coeff < coefftreble): coeff = coefftreble
          prevbass = prevbass*(coeffbass/coeff)
          prevmedium = prevmedium*(coeffmedium/coeff)
          prevtreble = prevtreble*(coefftreble/coeff)
          reason = 'A'
        else:
          prevbass = (prevbass*2+bass)/3
          prevmedium = (prevmedium*2+medium)/3
          prevtreble = (prevtreble*2+treble)/3
          reason = 'B'
        
        if (bass > prevbass): prevbass = bass
        if (medium > prevmedium): prevmedium = medium
        if (treble > prevtreble): prevtreble = treble
        #bass = math.floor((2*bass+prevbass)/3)
        #medium = math.floor((2*medium+prevmedium)/3)
        #treble = math.floor((2*treble+prevtreble)/3)
        bass = math.floor(100*prevbass/maxband)
        medium = math.floor(100*prevmedium/maxband)
        treble = math.floor(100*prevtreble/maxband)
 
        #print reason,' ; ',bass,' ; ',medium,' ; ',treble
        if (bass+medium+treble < 1): self.standby()
        else:
          self.sbcounter = -50
          led.setRed(bass)
          led.setGreen(medium)
          led.setBlue(treble)
        #prevbass = (bass+prevbass*6)/7
        #prevmedium = (medium+prevmedium*6)/7
        #prevtreble = (treble+prevtreble*6)/7
        self.SR.newAudio=False

  def stop(self):
    self.Terminated = True
    
  def sigterm_handler(self, _signo, _stack_frame):
    self.stop()


if __name__ != "__main__": sys.exit()

led=LED()

try:
  SR=SwhRecorder()
  SR.setup()
  SR.continuousStart()
  l = Listen(SR,led)
  signal.signal(signal.SIGTERM, l.sigterm_handler)
  l.loop()
except KeyboardInterrupt:
  pass

SR.continuousEnd()
l.stop()
SR.close()

