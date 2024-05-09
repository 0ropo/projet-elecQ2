import machine
import network
import socket
import utime
from machine import ADC

def connect():
    i=0
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("Hugo's Galaxy S20 FE 5G","akalazinedine")
    while not wlan.isconnected():
        print(f'en attente de connexion{i}')
        i+=1
        if i>=10:
            i = 0
        utime.sleep(2)
    ip = wlan.ifconfig()[0]
    print(f'Connecté avec l\'ip suivante {ip}')
    return ip

def open_socket(ip):
    address = (ip , 80)
    sock = socket.socket(socket.AF_INET)
    sock.bind(address)
    sock.listen(1)
    print(sock)
    return sock

def webpage(humidity):
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Plante for life</title>
            </head>
            <body>
            <h1>Elec Plante Autonome</h1>
            <!-- <from action="./on" >
            <input type="submit" value="Plante ON">
            </from>
            <from action="./off" >
            <input type="submit" value="Plante OFF">
            </from>
            <p>La plante est {state_plante}</p> -->
            <p>le taux d'humidité de la terre est de {humidity} %</p>
            </body>
            </html>
            """
    return str(html)
    

def serveWebPage(sock):
    state_led = 'OFF'
    led.off()
    temperature = 0
    while True :
        client = sock.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/ledON?':
            led.on()
            state_led = 'ON'
        elif request == '/ledOFF?':
            led.off()
            state_led = 'OFF'
        temperature = get_PICO_Temp()
        html = webpage(temperature , state_led)
        client.send(hmtl)
        client.close()

try:
    ip = connect()
    sock = open_socket(ip)
    serveWebPage(sock)
except KeyboardInterrupt:
    machine.reset()
