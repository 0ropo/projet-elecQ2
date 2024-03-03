from machine import ADC, Pin , PWM 
import utime
A0= ADC(27)
pwm0 = PWM(Pin(26))      # création d'un objet PWM lié à la broche 0
pwm0.freq(100)

while True:
    pass