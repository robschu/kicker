#Importe
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import RPi.GPIO as GPIO
import time
import pygame
import json
from game import Game
######################################################################
#####################           GPIO          ########################
######################################################################
######### Distanz zwischen Sensor und Oberflaeche  ###################
def distance():
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

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins zuweisen
GPIO_TRIGGER = 2
GPIO_ECHO = 3

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
abstand = distance()
wss =[]


#####################################################################
#####################          Websocket        #####################
############## Websocket Event Handler  #############################
class WSHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		 return True

	def open(self):
   		if self not in wss:
       			wss.append(self)
		print 'New connection was opened', self
    		    		 
  	def on_message(self, message):
    		print 'Incoming message:', message
		for ws in wss:
			if ws == self:
				self.write_message("You said: " + message)
			else:
				ws.write_message("Someone said: " + message) 
  	def on_close(self):
    		print 'Connection was closed...'
     		if self in wss:
      			wss.remove(self)



##############  Websocket Application  ##############################

application = tornado.web.Application([
  	(r'/ws', WSHandler),
])
#####################################################################
 
if __name__ == "__main__":
#####################################################################
################### WEbsocket Nachricht an alle #####################
#####################################################################
############## Konstanten ###########################################
	INTERVAL_MSEC = 2000
	
	def wsSend(message):
    		for ws in wss:
      			if not ws.ws_connection.stream.socket:
        			print "Web socket does not exist anymore!!!"
        			wss.remove(ws)
      			else:
        			ws.write_message(message)

################### Tor gefallen ? ##################################
############## Konstanten ###########################################
	VALUES_IN_AVERAGE = 5
	counter = 0
	last_distance_list = [1000]*VALUES_IN_AVERAGE

	def check_distance(get_distance,last_distance_list):
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
                        	wsSend(str(abstand)+ "Tor" + str(distance) + str(distance))
				Game1 = Game("Robert","blue")
				wsSend("--------------------------------")
				wsSend(Game1.toString())
	                        print("Gemessene Entfernung = %.1f cm" % abstand)#print
			counter = (counter + 1)% VALUES_IN_AVERAGE
                # Beim Abbruch durch STRG+C resetten
        	except KeyboardInterrupt:
                	print("Messung vom User gestoppt")
                	GPIO.cleanup()

#####################################################################
#####################################################################
################### Server starten ##################################
	http_server = tornado.httpserver.HTTPServer(application)
  	http_server.listen(8888)
    
  	main_loop = tornado.ioloop.IOLoop.instance()
  	sched_dist = tornado.ioloop.PeriodicCallback(
		lambda: check_distance(distance,last_distance_list),
		INTERVAL_MSEC,
		io_loop = main_loop)

  	sched_dist.start()
  	main_loop.start()

#####################################################################
