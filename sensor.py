import RPi.GPIO as GPIO
import time
######################################################################
#####################           GPIO          ########################
######################################################################
######### Distanz zwischen Sensor und Oberflaeche  ###################
def distance(trigger, echo):

        #GPIO Pins zuweisen
        GPIO_TRIGGER = trigger
        GPIO_ECHO = echo
        # setze Trigger auf HIGH
        GPIO.output(GPIO_TRIGGER, True)

        # setze Trigger nach 0.01ms aus LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartZeit = time.time()
        StopZeit = time.time()

        # speichere Startzeit
        while GPIO.input(GPIO_ECHO) == 0:
                StartZeit = time.time()

        # speichere Ankunftszeit
        while GPIO.input(GPIO_ECHO) == 1:
                StopZeit = time.time()

        # Zeit Differenz zwischen Start und Ankunft
        TimeElapsed = StopZeit - StartZeit
        # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
        # und durch 2 teilen, da hin und zurueck
        distanz = (TimeElapsed * 34300) / 2

        return distanz
        
################### Tor gefallen ? ##################################
############## Konstanten ###########################################
        VALUES_IN_AVERAGE = 5
        counter = 0
        last_distance_list = [1000]*VALUES_IN_AVERAGE


def check_distance_blue(get_distance,last_distance_list):
        global counter                                                                  
        try:    
                            
                tmpdist = get_distance()
                last_distance_list[counter] = tmpdist
                abstand = 0
                for distance in last_distance_list:
                        abstand += distance
                abstand = abstand / VALUES_IN_AVERAGE
                print "abstand: ", abstand
                if abstand < 100.0:
                        
                        wsSend(Game1.toString())
                        print("Gemessene Entfernung = %.1f cm" % abstand)#print
                counter = (counter + 1)% VALUES_IN_AVERAGE
        # Beim Abbruch durch STRG+C resetten
        except KeyboardInterrupt:
                print("Messung vom User gestoppt")
                GPIO.cleanup()

#####################################################################