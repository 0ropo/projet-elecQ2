from machine import Pin,PWM
import utime
from machine import ADC
import _thread
import sys
import time
import network
import socket
A = Pin(5,Pin.OUT)
B = Pin(4,Pin.OUT)
C = Pin(3,Pin.OUT)
D = Pin(2,Pin.OUT)
data = 0

transistor1 = Pin(15,Pin.OUT)
transistor2 = Pin(14,Pin.OUT)
adc = ADC(27)
binary_unit = '0000'
binary_dizaine = '0000'
servo_pin_number = 22
servo = PWM(Pin(servo_pin_number), freq=50)
A0= ADC(28)
pwm0 = PWM(Pin(0))  
pwm0.freq(100)


def readand_average(analog_in):
    analog_sum = 0
    for x in range(10):
        analog_sum += analog_in()
        utime.sleep(2)
    return analog_sum /10


def set_servo_angle(angle):
    pulse_width = (0.64 + angle/180*1.72)
    duty = pulse_width/20
    servo.duty_u16(int(duty*65535))
    time.sleep(1.5)

    
def arroserPlante(pourcentage):
    if int(pourcentage) <50:
        set_servo_angle(0)
        time.sleep(1.5)
        set_servo_angle(90)
        time.sleep(1.5)


def allumerLed():
    digital_value = A0.read_u16()     
    volt=5*(digital_value/65535)
    pwm0 = PWM(Pin(0))      
    pwm0.duty_u16( int((1/volt) *(65535/50) ))
    
    
def webpage(humidity,luminosity):
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="refresh" content="5">
                <title>Données de la plante auto-alimentée</title>
            </head>
            <body style="font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif; margin: 0; padding: 0; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; background-color: #e7fae2;">
                <h1 style="color: rgb(3, 155, 3); margin-bottom: 65px; font-size: 50px;">Données de la plante auto-alimentée</h1>
                <div class="parent" style="display: grid; grid-template-columns: repeat(2, 1fr); grid-template-rows: 1fr; grid-column-gap: 50px;">
                    <div class="div1" style="justify-content: center; align-items: center; background-color: #bfffbf; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin-bottom: 20px; margin-right: 20px; height: 250px; width: 300px; grid-area: 1 / 1 / 2 / 2;">
                        <p style="text-align: center; font-size: 30px; color: #3e3e3e;">Taux d'humidité</p>
                        <p class="pourcentage-humidite" style="font-size: 100px; text-align: center; margin: auto; color: rgb(3, 155, 3);">{humidity}%</p>
                    </div>
                    <div class="div2" style="justify-content: center; align-items: center; background-color: #bfffbf; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); margin-bottom: 20px; margin-right: 20px; height: 250px; width: 300px; grid-area: 1 / 2 / 2 / 3;">
                        <p style="text-align: center; font-size: 30px; color: #3e3e3e;">Taux de luminosité</p>
                        <p class="pourcentage-luminosite" style="font-size: 100px; text-align: center; margin: auto; color: rgb(3, 155, 3);">{luminosity}%</p>
                    </div>
                </div>

                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        const humidityBox = document.querySelector('.div1');
                        const humidityText = humidityBox.querySelector('.pourcentage-humidite');
                        const humidityValue = parseInt(humidityText.textContent);

                        const luminosityBox = document.querySelector('.div2');
                        const luminosityText = luminosityBox.querySelector('.pourcentage-luminosite');
                        const luminosityValue = parseInt(luminosityText.textContent);

                        function applyStyles(box, text, value) {{
                            if (value < 21) {{
                                box.style.backgroundColor = '#ffcccc';
                                text.style.color = '#ff0000';
                            }} else if (value >= 20 && value < 51) {{
                                box.style.backgroundColor = '#ffe0b3';
                                text.style.color = '#ff8000';
                            }} else {{
                                box.style.backgroundColor = '#bfffbf';
                                text.style.color = 'rgb(3, 155, 3)';
                            }}
                        }}

                        applyStyles(humidityBox, humidityText, humidityValue);
                        applyStyles(luminosityBox, luminosityText, luminosityValue);
                    }});
                </script>
            </body>
            </html>
            """
    return str(html)


def serveWebPage(sock,humidity):
    while True :
        client = sock.accept()[0]
        html = webpage(humidity)
        client.send(html)
        client.close()


def threading():   
    global data, A, B, C, D, transistor1, transistor2 
    while True:
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
        allumerLed()
        
    
_thread.start_new_thread(threading,())
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("Hugo's Galaxy S20 FE 5G","akalazinedine")

while not wlan.isconnected():
        print('Waiting for connection...')
        utime.sleep(1)
        
        
ip = wlan.ifconfig()[0]
print(f"co sur {ip}")
address = (ip , 80)

sock = socket.socket()
sock.bind(address)
sock.listen(1)
print(sock)

while True:
    print(ip)
    digital_value = A0.read_u16()     
    volt=5*(digital_value/65535)
    raw_value = adc.read_u16()
    data = 100 - ((raw_value/65535)*100)

    if(data < 50):
        set_servo_angle(40)
        
        
    set_servo_angle(100)

    client = sock.accept()[0]
    request = client.recv(1024)
    request = str(request)
    print(request)
    html = webpage(int(data),int(((volt/5)*100)))
    client.sendall(html)
    client.close()
    
