from machine import Pin 

def init_leds():
    for i in range(4):
         led = Pin(i)
         led.init(Pin.OUT)

while True:
  pass
