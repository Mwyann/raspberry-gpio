#!/usr/bin/python
import socket,threading,time,math
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
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
	if v>=0 and v<=100: r.ChangeDutyCycle(calcLog(v))
def setGreen(v):
	if v>=0 and v<=100: g.ChangeDutyCycle(calcLog(v))
def setBlue(v):
	if v>=0 and v<=100: b.ChangeDutyCycle(calcLog(v))

class Connection:

  def __init__(self,client):  ## Constructeur
    self.client = client
    self.Terminated = False

  def loop(self):
    while not self.Terminated:
      d = self.client.recv(1024)
      lines = d.split('\n')
      for l in lines:
        if l[:4] == 'exit':
          self.disconnect()
          return
        c = l.split(' ')
        if len(c) > 2:
          setRed(int(c[0]))
          setGreen(int(c[1]))
          setBlue(int(c[2]))

  def disconnect(self):
    if not self.Terminated:
      print 'Closing connection'
      self.client.close()
      self.Terminated = True

  def stop(self):
    self.disconnect()


host = ''
port = 5050
backlog = 5
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(backlog)
clientlist=[]
print "Listening"
try:
  while 1:
    client, address = s.accept()
    pwmconn = Connection(client)
    t = threading.Thread(None, pwmconn.loop, None, (),{})
    t.start()
    clientlist.append(pwmconn)
    print 'Someone\'s connected.'
except KeyboardInterrupt:
    pass

for t in clientlist:
  t.stop()
print 'Bye.'
s.shutdown(socket.SHUT_RDWR)
s.close()
r.stop()
g.stop()
b.stop()
GPIO.cleanup()

