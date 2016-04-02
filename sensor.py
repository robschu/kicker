import RPi.GPIO as GPIO
import time
######################################################################
#####################           GPIO          ########################
######################################################################
######### Distanz zwischen Sensor und Oberflaeche  ###################
class goalWatch(object):
	def __init__(self,trigger,echo,side):
		self.trigger = trigger
		self.echo = echo
		self.side = side
		self.VALUES_IN_AVERAGE = 1
		self.counter = 0
		self.last_distance_list = [1000]*self.VALUES_IN_AVERAGE

	def distance(self):

	        #GPIO Pins zuweisen
        	GPIO_TRIGGER =self.trigger
        	GPIO_ECHO = self.echo
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

	def check_distance(self,game):				
		try:    
			            
                	tmpdist = self.distance()
			self.last_distance_list[self.counter] = tmpdist
			abstand = 0
			for distance in self.last_distance_list:
				abstand += distance
			abstand = abstand / self.VALUES_IN_AVERAGE
			print "abstand: ", abstand
                        if abstand < 200.0:
        		        game.goal(str(self.side))
                        	self.counter = (self.counter + 1)% self.VALUES_IN_AVERAGE
	                        print( ": Gemessene Entfernung = %.1f cm" % abstand)
				return game
       			print self.side,"nobody is gonna see this! REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"                          
			return 0            
                # Beim Abbruch durch STRG+C resetten
        	except KeyboardInterrupt:
                	print("Messung vom User gestoppt")
                	GPIO.cleanup()
