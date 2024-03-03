from machine import ADC
import utime


# Configuration de la broche analogique
adc = ADC(28)

while True:
    # Lecture de la valeur analogique brute
    raw_value = adc.read_u16()
