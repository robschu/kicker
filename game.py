import json

class Game(object):

	def __init__(self, player_name, side):
		self.gameid = "Training"
		if(side == "blue"):
			self.team_blue_player_name1 = player_name
                        self.team_red_player_name1 = " "

		else:
			self.team_red_player_name1 = player_name
                        self.team_blue_player_name1 = " "
                self.team_blue_player_name2 = " "
		self.team_red_player_name2 = " "		

		self.team_blue_goals = "0"
		self.team_red_goals = "0"
		
	def toString(self):
		
		resultString = '{"game": {"gameid" : "' + self.gameid + '","team" : [{"blue" : {"player" :[{"name" :"'+ self.team_blue_player_name1+'"},{"name" :"'+ self.team_blue_player_name2+'"}], "goals" : "'+self.team_blue_goals+'"}},{"red"  : {"player" :[{"name" :"'+self.team_red_player_name1+'"},{"name" :"'+self.team_red_player_name2+'"}], "goals" : "'+self.team_red_goals+'"}}]}}'
		return resultString
