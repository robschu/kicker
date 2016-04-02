#Importe
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import RPi.GPIO as GPIO
from game import Game
from sensor import goalWatch

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins zuweisen
GPIO_TRIGGER_BLUE = 2
GPIO_ECHO_BLUE = 3

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER_BLUE, GPIO.OUT)
GPIO.setup(GPIO_ECHO_BLUE, GPIO.IN)

goalWatch_blue = goalWatch(GPIO_TRIGGER_BLUE,GPIO_ECHO_BLUE,"blue")

Game1 = Game()

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
    		self.write_message(Game1.toString())    		 
  	def on_message(self, message):
    		print 'Incoming message:', message
		if message == "increaseBlue":
			Game1.goal("blue")
			wsSend(Game1.toString())	
		if message == "increaseRed":
			Game1.goal("red")
			wsSend(Game1.toString())
		if message == "reset":
			Game1.resetGoals()
			wsSend(Game1.toString())
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
	INTERVAL_MSEC = 100
	
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
		global Game1				
		try:    
			            
                	tmpdist = get_distance()
			last_distance_list[counter] = tmpdist
			abstand = 0
			for distance in last_distance_list:
				abstand += distance
			abstand = abstand / VALUES_IN_AVERAGE
			print "abstand: ", abstand
                        if abstand < 100.0:
        		        Game1.goal("blue")
	                       	wsSend(Game1.toString())
	                        print("Gemessene Entfernung = %.1f cm" % abstand)#print
                        if abstand > 200.0:
                                Game1.goal("red")
                          	wsSend(Game1.toString())
                          
			counter = (counter + 1)% VALUES_IN_AVERAGE
                # Beim Abbruch durch STRG+C resetten
        	except KeyboardInterrupt:
                	print("Messung vom User gestoppt")
                	GPIO.cleanup()

#####################################################################
#####################################################################
################### Server starten ##################################
	
	Game1.addPlayer("Mirko","red")
	Game1.addPlayer("Viktor","blue")
	Game1.addPlayer("Robert","blue")
	Game1.addPlayer("Philipp","red")
	wsSend(Game1.toString())
                          
	http_server = tornado.httpserver.HTTPServer(application)
  	http_server.listen(8888)
    
  	main_loop = tornado.ioloop.IOLoop.instance()
  	goal_watch_blue = tornado.ioloop.PeriodicCallback(
		lambda: goalWatch_blue.check_distance(
    		Game1),
		INTERVAL_MSEC,
		io_loop = main_loop)

  	goal_watch_blue.start()
  	main_loop.start()

#####################################################################
