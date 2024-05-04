from machine import Pin,PWM,ADC
import utime
import _thread
import sys
import time


A = Pin(5,Pin.OUT)
B = Pin(4,Pin.OUT)
C = Pin(3,Pin.OUT)
D = Pin(2,Pin.OUT)

transistor1 = Pin(15,Pin.OUT)
transistor2 = Pin(14,Pin.OUT)
adc = ADC(27)
binary_unit = '0000'
binary_dizaine = '0000'
servo_pin_number = 22
servo = PWM(Pin(servo_pin_number), freq=50)
pwm0 = PWM(Pin(0))      # création d'un objet PWM lié à la broche 0
pwm0.freq(100)
A0 = ADC(28)

def set_servo_angle(angle):
    pulse_width = (0.64 + angle / 180 * 1.72)
    duty = pulse_width / 20
    servo.duty_u16(int(duty * 65535))
    print("Angle:", angle)
    print("Duty cycle:", duty)

def threading():
    while True:
            
        #raw_value = adc.read_u16()
        #raw_value = 57671
        raw_value = adc.read_u16()
            #raw_value = 57671
        data = (raw_value/65535) / 100
        print(data)
        dizaine=data/10
        unite = data%10
        
        binary_unit=f'{int(unite):04b}'
        binary_dizaine=f'{int(dizaine):04b}'
        
        A.value(int(binary_unit[-1]))
        B.value(int(binary_unit[-2]))
        C.value(int(binary_unit[-3]))
        D.value(int(binary_unit[-4]))
        transistor1.value(1)
        utime.sleep_ms(5)
        transistor1.value(0)

        A.value(int(binary_dizaine[-1]))
        B.value(int(binary_dizaine[-2]))
        C.value(int(binary_dizaine[-3]))
        D.value(int(binary_dizaine[-4]))
        transistor2.value(1)
        utime.sleep_ms(5)
        transistor2.value(0)
        

_thread.start_new_thread(threading,())


while True:
    
    set_servo_angle(0)
    time.sleep(1.5)
    set_servo_angle(60)
    time.sleep(1.5)
    
    digital_value = A0.read_u16()
    volt=3.3*(digital_value/65535)
    pwm0 = PWM(Pin(0))
    pwm0.duty_u16( int((1/volt) *(65535/50) ))
    utime.sleep_ms(5)
