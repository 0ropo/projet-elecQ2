from machine import Pin 

def init_leds():
    for i in range(4):
         led = Pin(i)
         led.init(Pin.OUT)

def set_leds(x):
    for i in range(4): # pin 0 à 3
         led = Pin(i)
         led.value(  (x>>i)%2 )

init_leds()
set_leds(8)
while True:
  sleep(1)
