import RPi.GPIO as GPIO
from game import Game
from sensor import goalWatch
#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#GPIO Pins zuweisen
GPIO_TRIGGER_BLUE = 14
GPIO_ECHO_BLUE = 15

#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER_BLUE, GPIO.OUT)
GPIO.setup(GPIO_ECHO_BLUE, GPIO.IN)

Game1 = Game()
goalWatch_blue = goalWatch(GPIO_TRIGGER_BLUE,GPIO_ECHO_BLUE,"blue")
print goalWatch_blue.distance()

goalWatch_blue.check_distance_blue(Game1)
