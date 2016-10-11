import RPi.GPIO as GPIO
######################################################################
#####################           GPIO          ########################

######################################################################
######### Distanz zwischen Sensor und Oberflaeche  ###################
class goalWatch(object):
	def __init__(self,receiver,side):
		self.receiver = receiver
		self.side = side

		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.receiver, GPIO.IN)

	def check_sensor(self,game):
		try:                
			if GPIO.input(self.receiver) == 1:
				print GPIO.input(self.receiver)
				game.goal(str(self.side))
				return game
			return 0   

		# Beim Abbruch durch STRG+C resetten
		except KeyboardInterrupt:
			print("Messung vom User gestoppt")
			GPIO.cleanup()
