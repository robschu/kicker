#Importe
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import RPi.GPIO as GPIO
import json
from game import Game
import sensor

#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins zuweisen
GPIO_TRIGGER_BLUE = 2
GPIO_ECHO_BLUE = 3

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER_BLUE, GPIO.OUT)
GPIO.setup(GPIO_ECHO_BLUE, GPIO.IN)

abstand = sensor.distance(GPIO_TRIGGER_BLUE,GPIO_ECHO_BLUE)

Game1 = Game()
Game1.addPlayer("Mirko","rot")
Game1.addPlayer("Robert","blau")
Game1.addPlayer("Viktor","rot")
Game1.addPlayer("Philipp","blau")



wss_clients =[]


#####################################################################
#####################          Websocket        #####################
############## Websocket Event Handler  #############################
class WSHandler(tornado.websocket.WebSocketHandler):
	def check_origin(self, origin):
		 return True

	def open(self):
   		if self not in wss_clients:
       			wss_clients.append(self)
		print 'New connection was opened', self
    		    		 
  	def on_message(self, message):
    		print 'Incoming message:', message
		for ws_client in wss_clients:
			print ws_client
			if ws_client == self:
				self.write_message("You said: " + message)
			else:
				ws_client.write_message("Someone said: " + message) 
  	def on_close(self):
    		print 'Connection was closed...'
     		if self in wss_clients:
      			wss_clients.remove(self)



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
    		for ws_client in wss_clients:
      			if not ws_client.ws_connection.stream.socket:
        			print "Web socket does not exist anymore!!!"
        			wss_clients.remove(ws_client)
      			else:
        			ws_client.write_message(message)


#####################################################################
################### Server starten ##################################
	http_server = tornado.httpserver.HTTPServer(application)
  	http_server.listen(8888)
    
  	main_loop = tornado.ioloop.IOLoop.instance()

  	goal_watch_blue = tornado.ioloop.PeriodicCallback(
		lambda: sensor.check_distance_blue(
    lambda: sensor.distance(GPIO_TRIGGER_BLUE,GPIO_ECHO_BLUE),
    last_distance_list),
		INTERVAL_MSEC,
		io_loop = main_loop)

  	goal_watch_blue.start()
  	main_loop.start()

#####################################################################
