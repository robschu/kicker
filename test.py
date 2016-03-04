from game import Game

Game1 = Game()

print Game1.toString()

Game1.addPlayer("blue1",'blue')

Game1.addPlayer("blue2",'blue')

Game1.addPlayer("Rot1",'red')

Game1.addPlayer("Rot2",'red')

print Game1.toString()

Game1.removePlayer("Rot1",'red')

print Game1.toString()

Game1.removePlayer("blue1","blue")

print Game1.toString()

Game1.removePlayer(' ','red')

print Game1.toString()
