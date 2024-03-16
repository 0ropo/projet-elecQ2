from machine import ADC, Pin , PWM 
import utime
A0= ADC(27)
pwm0 = PWM(Pin(26))      
pwm0.freq(100)

while True:
    digital_value = A0.read_u16()     
    
    volt=3.3*(digital_value/65535)
    
    

    pwm0 = PWM(Pin(26))      
    pwm0.duty_u16( int((1/volt) *(65535/50) )) 
        
        
    utime.sleep_ms(100)