"""
Author : Vincent Tanguay Casgrain
Date: 2017-08-10
"""
import deck as d
import player as p
from cerberus import Validator

class Game:

	def __init__(self, deck=[]):

		self.players = []
		self.dealers = []
		self.Default_dealer = []


		if not deck:
			print("Instanciation of a Game Class requiere a Deck Class")
			return

		if not isinstance(deck, d.Deck):
			print("Function take Deck Class as Input. Empty deck for now.")
			return

		else:
			self.deck = deck
		
		self.Default_dealer = p.Player(player_type = "Dealer",name="The Dealer")
		self.Default_dealer.stand_on = 17
		self.players.append(self.Default_dealer)
		self.game_count = 0 

	def add_players(self,*players):

		for player in players:

			if isinstance(player, p.Player):

				self.players.append(player)

			else:
				print("That's not a Class Player")
				return None

		return True

	def get_players_names(self):
		temp_players = []

		for player in self.players:
			temp_players.append(player.name)

		return temp_players

	def place_bets(self):

		for player in self.players:
			if player.type is  "Gambler":
				player.bet()

	def pay(self,player,times):

		if not isinstance(player, p.Player):
			print("Function take a Player Class as Input.")
			return 0 
		player.money += (player.pbet  * times)

	def play_round(self, player_type,deck):

		for player in self.players:

			if (player.type == player_type):

				player.play(deck,self.players)


	def compare(self):

		if self.Default_dealer.has_busted:
			self.Default_dealer.bust_count += 1

			for player in self.players:

				if player.type ==  "Gambler" and not player.has_busted:

					player.victory += 1
					self.pay(player,times=2)
					self.Default_dealer.loss += 1	

			self.Default_dealer.has_busted = False
			return 1

		
		for player in self.players:

			if player.type ==  "Gambler":

				if  player.total > self.Default_dealer.total and not player.has_busted:
					#print player.name + " beats the dealer"
					player.victory += 1
					self.pay(player,times=2)
					self.Default_dealer.loss += 1
					pass

				elif player.total == self.Default_dealer.total:
					self.pay(player,times=1)
					pass

				else:
					#print "The dealer win the hand"
					if player.has_busted:
						player.bust_count += 1
					
					player.loss += 1
					self.Default_dealer.victory += 1
					pass

		return 0

	def pass_cards(self,number_of_cards):

		if not self.deck.deck:
			print("Deck Is empty---- ")
			return False
			
		for i in range(number_of_cards):
			for player in self.players:

				player.hit(self.deck)

		return True
	
	def give_stats_to_players(self,stat):

		schema = {'Stats obj': {'allowed':['Stats']}}
		v = Validator(schema)

		if not v.validate({'Stats obj': [stat.__class__.__name__]}):
			raise Exception(v.errors,"Allowed Type:" + stat.__class__.__name__)

		for player in self.players:
			player.request_game_stats(stat)
		
	def show_player_stats(self):

		if not self.players:
			Print("The Game has no Player!!")
			return False

		for player in self.players:
			if player.__dict__:
				player.show_stats()

	def show_adv_player_stats(self):

		if not self.players:
			Print("The Game has no Player!!")
			return False

		for player in self.players:
			if player.__dict__:
				player.show_adv_stats()
				print('\n')

	def flush_hand(self):

		for player in self.players:

			player.flush_hand()



if __name__ == '__main__':

	
	deck = d.Deck()
	deck.initialize(number_of_card=52,random_order=True)

	player1 = p.Player(player_type = "Gambler", name="Player One")

	game = Game(deck)

	game.add_players(player1)

	for i in range(1):

		game.pass_cards(2)
		game.show_player_stats()

		game.flush_hand()




		# game.show_player_stats()

		# game.play_round()
