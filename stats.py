#!/usr/bin/python

import game as g
import numpy as np
import ui 
from cerberus import Validator
import math 

class Stats:
	__stat_type = ['wins','bust','money','bust_slope','bet_size']

	def __init__(self, game):
		"""
		The stat class collect every stat about the game.
		TODO Complete revamp. no longer give a specific stats to the player, the player get all the stats then choose
		what to do with it
		:param game:
		"""

		if not game:
			print("Instanciation of a Game Class requiere a game Class")
			return

		schema = {'game Type': {'allowed':['Game']}}
		v = Validator(schema)

		if not v.validate({'game Type': [game.__class__.__name__]}):
			print(v.errors)
			print("Allowed Type:" +' Game')

		#naming convention for data is name_data
		self.data_wins = np.empty([0, 0])
		self.data_money = np.empty([0, 0])
		self.data_bust = np.empty([0, 0])
		self.data_bust_slope = np.empty([0, 0])
		self.data_bet_size = np.empty([0, 0])

		#naming convention for history is name_buffer
		self.buffer_bust_slope = []
		self.buffer_wins = []
		self.buffer_bust = []
		self.buffer_money = []
		self.buffer_bet_size =[]
		
		self.bjgame = game
		self.numb_of_players = len(self.bjgame.players)

		# When calculating the slope, this is the Dx (over how many point you do the slope)
		self.slope_width = 10 #default

	def update_stats(self):
		"""
		Scan all the player for thiers stats
		it appends to a buffer so you can plot it in a graph
		:return: a pointer to itself
		"""

		for players in self.bjgame.players:
			self.buffer_wins.append(players.victory)
			self.buffer_money.append(players.money)
			self.buffer_bust.append(players.bust_count)
			self.buffer_bet_size.append(players.pbet)

			self.differential(self.buffer_bust, self.buffer_bust_slope, players.bust_count)

		return self

	def differential(self, data_buffer, data_slopes_buffer, player_var):
		"""
		Do a derevative of a specific stats
		:param data_buffer: A data array / list
		:param data_slopes_buffer: the data array / list of slopes? Not ever sure myself
		:param player_var: The variable to differentiate
		:return: NA
		"""

		#not sure what this do anymore
		if len(data_buffer) > self.numb_of_players * self.slope_width:
			data_slopes_buffer.append(self.slope(player_var, data_buffer[-((self.numb_of_players * self.slope_width)+1)]))

		elif len(data_buffer) <= self.numb_of_players:
			data_slopes_buffer.append(0)

		else:
			data_slopes_buffer.append(self.slope(player_var, data_buffer[-(self.numb_of_players + 1)]))
			

	def give_stats_to_player(self, stat_type):
		"""
		Give desired stats to a player. The stat they want depends on which playstyle they have
		TODO scrap this
		:param stat_type:
		:return:
		"""

		schema = {'Stat Type':{'allowed': self.__stat_type}}
		v = Validator(schema)

		if not v.validate({'Stat Type':[stat_type]}):
			raise Exception(v.errors,"Allowed Type:" + __stat_type + "for stat type")

		if stat_type == "Bust_Slope":
			return self.buffer_bust_slope[-(self.numb_of_players)]

		return 0

	def shape_graph(self, buff, array):
		"""
		shape the data list to match the data structure for plotting
		:param buff: Buffers of this class (e.i : bust_slopes_buffer)
		:param array: Something that will be transformed in numpy arrays for matplotlib
		:return:
		"""

		array = np.asarray(buff)
		return np.reshape(array, (int(len(buff)/self.numb_of_players), self.numb_of_players))


	def show_all(self, data_to_show_list = __stat_type):
		"""
		Fonction to show all the graphs and all the stats
		:return: return False if no data was requested
		"""

		if not isinstance(data_to_show_list, list):
			raise(TypeError("Data to show need to be in a list"))

		# Removing space and capital letters
		try:
			data_to_show_list = [x.lower().strip() for x in data_to_show_list]
		except:
			pass

		count = 0
		names = self.bjgame.get_players_names()

		for key1 in self.__dict__.keys():
			ksplit = key1.split('_', 1)

			if "data" in ksplit:
				# The whole data key
				data_key = key1

				# first index of the split is data, check for the name within the second index
				key_name = ksplit[1]

				# check if the value is actually requested
				if key_name in data_to_show_list:
					count += 1

					for buffer_key in self.__dict__.keys():
						if "buffer_" + key_name == buffer_key:

							self.__dict__[data_key] = self.shape_graph(self.__dict__[buffer_key], self.__dict__[data_key])
							self.show_data(key_name, names, self.__dict__[data_key], self.__dict__[buffer_key])

							# Break the second for loop for speed
							break

		if count == 0:
			print("Simulation did not request data or either the data name are wrong. Allowed data are:\n {0}". format(self.__stat_type))
			return False

		return True

	def show_data(self, label, names, points, buff):
		self.shape_graph(buff, points)
		try :
			graph = ui.Graphs(label, points,names)
			graph.start()

		except ValueError:
			raise(ValueError("something went wrong in graphs"))

	def slope(self, y2, y1):
		return (y2-y1)
    	

if __name__ == '__main__':

	import deck as d
	import player as p
	
	deck = d.Deck()
	deck.initialize(number_of_card=10,random_order=True)

	player1 = p.Player(player_type = "Gambler", name="Player One")

	game = g.Game(deck)

	game.add_players(player1)#,player2,player3)

	s = Stats(game)