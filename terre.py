from machine import ADC
import utime


# Configuration de la broche analogique
adc = ADC(28)

while True:
    # Lecture de la valeur analogique brute
    raw_value = adc.read_u16()
    
    # Conversion de la valeur analogique en pourcentage d'humidité
    # Supposons que la valeur lue soit entre 0 (sécheresse) et 65535 (humide)
    moisture_percentage = (raw_value / 65535) * 100
    
    # Affichage du pourcentage d'humidité
    print("Moisture Percentage:", 100 - moisture_percentage, "%")
    
    # Attente de 10 secondes avant la prochaine lecture
    


    # Attente de 10 secondes avant la prochaine lecture
    utime.sleep_ms(500)