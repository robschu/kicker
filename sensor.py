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


