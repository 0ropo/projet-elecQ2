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


