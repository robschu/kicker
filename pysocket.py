##Importe
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
GPIO_TRIGGER_RED = 14
GPIO_ECHO_RED = 15

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER_BLUE, GPIO.OUT)
GPIO.setup(GPIO_ECHO_BLUE, GPIO.IN)
#GPIO.setup(GPIO_TRIGGER_RED, GPIO.OUT)
#GPIO.setup(GPIO_ECHO_RED, GPIO.IN)


goalWatch_blue = goalWatch(GPIO_TRIGGER_BLUE,GPIO_ECHO_BLUE,"blue")
goalWatch_red = goalWatch(GPIO_TRIGGER_RED,GPIO_ECHO_RED,"red")


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
	INTERVAL_MSEC = 50
		
	def wsSend(message):
    		for ws in wss:
      			if not ws.ws_connection.stream.socket:
        			print "Web socket does not exist anymore!!!"
        			wss.remove(ws)
      			else:
        			ws.write_message(message)
#####################################################################
##############Sendeloop##############################################
	def send_changes():
		print 2



################### Tor gefallen ? ##################################
############## Konstanten ###########################################
# evtl goalWatch blue und Red zusammenfassen, dann kann man sie leichter stoppen um aenderungen an clients zu pushen
	def check_goal(goalWatch):
		global Game1
		tempGame = goalWatch.check_distance(Game1)
		try:
			newGameString = tempGame.toString()
			Game1 = tempGame
			print "wsSend wegen !=0" + newGameString
			wsSend(newGameString)
		except AttributeError:
			print "tempGame hatte kein toString()"
		except:
			print "unknown error"
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
		lambda: check_goal(
    		goalWatch_blue),
		INTERVAL_MSEC,
		io_loop = main_loop)

        goal_watch_red = tornado.ioloop.PeriodicCallback(
                lambda: check_goal(
                goalWatch_red),
	        INTERVAL_MSEC,
                io_loop = main_loop)

#	goal_watch_red.start()
  	goal_watch_blue.start()
  	main_loop.start()

#####################################################################
