class Game(object):

	def __init__(self):
		self.gameid = "Training"

                self.team_red_player_name1 = ' '
                self.team_blue_player_name1 = ' '
                self.team_blue_player_name2 = ' '
		self.team_red_player_name2 = ' '		

		self.team_blue_goals = "0"
		self.team_red_goals = "0"
		
	def toString(self):
		
		resultString = '{"game": {"gameid" : "' + self.gameid + '","team" : [{"blue" : {"player" :[{"name" :"'+ self.team_blue_player_name1+'"},{"name" :"'+ self.team_blue_player_name2+'"}], "goals" : "'+self.team_blue_goals+'"}},{"red"  : {"player" :[{"name" :"'+self.team_red_player_name1+'"},{"name" :"'+self.team_red_player_name2+'"}], "goals" : "'+self.team_red_goals+'"}}]}}'
		return resultString

	def addPlayer(self, player_name, side):
#		print side		
		if side == 'blue' and (self.team_blue_player_name1 == ' ' or self.team_blue_player_name2 == ' '):
			if self.team_blue_player_name1 == ' ':
#				print "blue player1"
				self.team_blue_player_name1 = player_name
			else:
#				print "side is not blue and player 2"
				self.team_blue_player_name2 = player_name
		elif side == 'red' and ( self.team_red_player_name1 == ' ' or self.team_red_player_name2 == ' '):
 #                       print "red"
			if self.team_red_player_name1 == ' ':
                                self.team_red_player_name1 = player_name
                        else:
                                self.team_red_player_name2 = player_name
 		else:
			print "side not red or blue"
#			self.error_message = 'Team is already full'
	def removePlayer(self, player_name, side):
		 if side == 'blue': 
			if self.team_blue_player_name2 == player_name:
				self.team_blue_player_name2 = ' '
                        if self.team_blue_player_name1 == player_name:
                                self.team_blue_player_name1 = ' '
                 if side == 'red':
                        if self.team_red_player_name2 == player_name:
                                self.team_red_player_name2 = ' '
                        if self.team_red_player_name1 == player_name:
                                self.team_red_player_name1 = ' '
	def goal(self,side):
		if side == 'red':
			self.team_red_goals = str(int(self.team_red_goals) + 1)
		if side == 'blue':
			self.team_blue_goals = str(int(self.team_blue_goals) + 1)

	def resetGoals(self):
		self.team_red_goals  = "0"
		self.team_blue_goals = "0"		
