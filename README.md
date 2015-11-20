# raspberry-gpio

Just a simple bunch of Python scripts that uses gpio pins on a Raspberry-pi and a few transistors to control a RGB led strip according to music recorded from an USB soundcard (red is bass, green is medium, blue is treble).

You can watch a demonstration here: https://www.youtube.com/watch?v=9YA7A3smi-o

Files:
* example-basic.py : will just make the pin 12 flicker. No PWM used here.
* example-pwm.py : will make the pin 15 go up and down, using PWM. Just to make sure everything works.
* pwm-server.py : when run, it opens a TCP server at port 5050 (by default), and when you connect to it by telnet, it accepts 3 numbers, space separated, from 0 to 100, which represents the RGB color values to display. You can hook it to a piece of software that will do the DSP instead of the raspberry if needed. And at last if you type in the word "exit" it just closes the connexion.
* pwm.py : a cleaner example of PWM fading, using multiple colors and the use of a function that converts color values from lin to log.
* pwmled.py : this is a class to control the leds, including the lin-to-log function.
* recorder.py : this is a class that is used to control and record from a soundcard (here from an USB card). It also integrates a fft function to get the values for the different frequencies.
* usb.py : and finally, the program that does all the magic, combining pwmled and recorder. It containes a pretty nasty algorithm that tries to make a nice color effect, trying to prevent the flickering effect and also trying to make colors pop a little bit more.

This is just a proof-of-concept (why would you prove that anyway). It's badly written, and it barely works. The algorithm inside usb.py has been found by trial and errors and is very perfectible. It's up to you I guess...
