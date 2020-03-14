"""
Author : Vincent Tanguay Casgrain
Date: 2017-08-10
"""
import deck as d
import player as p
import stats as s
from cerberus import Validator

class Game:
	"""
	The Game Object
	Represent the dealer and the table
	So it has all the methode of a table or a should do

	:Init: Takes a deck of card
	"""

	def __init__(self, deck=[]):
		"""
		Init of the class
		:param deck: a deck of card (class deck)
		"""

		self.players = []
		self.dealers = []
		self.Default_dealer = []

		if not deck:
			raise(TypeError("Instanciation of a Game Class requiere a Deck Class"))

		if not isinstance(deck, d.Deck):
			raise(TypeError("Function take Deck Class as Input. Empty deck for now."))

		else:
			self.deck = deck

		#set the first player as the dealer
		self.Default_dealer = p.Player(player_type = "Dealer", name="The Dealer")
		self.Default_dealer.stand_on = 17
		self.players.append(self.Default_dealer)

		self.game_count = 0
		self.true_count = 0.0
		self.decks_remaining = self.get_remaing_deck()

		self.stats = None

	def add_players(self, *players):
		"""
		Add player(s) to the game
		:param players: Any number of player
		:return: True if added, None if there was a problem
		"""

		#check if input is of class player and then adds them to the game player list
		for player in players:
			if isinstance(player, p.Player):
				self.players.append(player)

			else:
				print("That's not a Class Player")
				return None

		return True

	def add_stats_obj(self):
		"""
		Proper way to instanciate stats obj
		:return: NA
		"""
		self.stats = s.Stats(self)

	def get_players_names(self):
		"""
		get the player name attribute
		:return: A liste of player names
		"""
		temp_players = []

		for player in self.players:
			temp_players.append(player.name)

		return temp_players

	def get_remaing_deck(self):
		return int(self.deck.cards_remaning() / 52)

	def place_bets(self):
		"""
		Place the bets of the player
		Calls the bet function of the player
		:return: NA
		"""
		for player in self.players:
			if player.type is  "Gambler":
				player.bet()

	def pay(self, player, times):
		"""
		Pay the player the number of time according to the game they played (usually its x2)
		:param player: the player (placer class)
		:param times: multiple (e.i 2x)
		:return: 0 if something went wrong
		"""

		if not isinstance(player, p.Player):
			print("Function take a Player Class as Input.")
			return 0 
		player.money += (player.pbet  * times)

	def play_round(self, player_type, deck):
		"""
		Calls the play fonction of the player
		Check the player type as if its a gambler or the dealer (only play the givin type)
		:param player_type: The type of the players to play
		:param deck: A deck of card (Deck class)
		:return: TODO returns who played
		"""

		for player in self.players:
			if (player.type == player_type):
				player.play(deck, self.players)


	def compare(self):
		"""
		the compare function check the cards of each player and compare it with the dealer
		and declare who wins and who loose
		then call the pay fonction
		:return: 1 if the dealer has busted, 0 if not
		"""

		#first, check if the dealer has busted
		if self.Default_dealer.has_busted:
			self.Default_dealer.bust_count += 1

			for player in self.players:
				#check if the player has busted
				if player.type == "Gambler" and not player.has_busted:

					player.victory += 1
					self.pay(player, times=2)
					self.Default_dealer.loss += 1	

			self.Default_dealer.has_busted = False
			return 1

		#then compare with everyplayer to compare card and declare the winner
		for player in self.players:

			if player.type ==  "Gambler":

				if  player.total > self.Default_dealer.total and not player.has_busted:

					player.victory += 1
					self.pay(player, times=2)
					self.Default_dealer.loss += 1
					pass

				elif player.total == self.Default_dealer.total:
					self.pay(player, times=1)
					pass

				else:

					if player.has_busted:
						player.bust_count += 1
					
					player.loss += 1
					self.Default_dealer.victory += 1
					pass

		return 0

	def pass_cards(self, number_of_cards):
		"""
		Pass the card to the player
		:param number_of_cards: how many card to pass (2 initially)
		TODO :player: pass a card to this specific player
		:return: False error , true if completed
		"""

		if not self.deck.deck:
			print("Deck Is empty---- ")
			return False

		#pass the number of card to all the players
		for i in range(number_of_cards):
			for player in self.players:

				card = player.hit(self.deck)

				try:
					value = card.conversion()
				except AttributeError:
					return False

				if value >= 10:
					self.game_count -= 1
				elif value > 6 or value > 10:
					pass
				else:
					self.game_count += 1

		return True
	
	def give_stats_to_players(self):
		"""
		TODO delete this function and pass the stats everyround
		Every type of player requiered a stats for thier gamestyle.
		This fonction give the asked stat to the player
		:param stat: which stat to pass out
		:return:  NA
		"""

		if self.stats == None:
			raise(ValueError("No stats object"))

		#TODO just give evrything to everybody instead of specific
		for player in self.players:
			player.request_game_stats(self.stats)
		
	def show_player_stats(self):
		"""
		Calls the player stats fonction
		:return:  NA
		"""
		if not self.players:
			print("The Game has no Player!!")
			return False

		for player in self.players:
			#????
			if player.__dict__:
				player.show_stats()

	def show_adv_player_stats(self):
		"""
		show more detailed stats for players
		:return:
		"""

		if not self.players:
			print("The Game has no Player!!")
			return False

		for player in self.players:
			#????
			if player.__dict__:
				player.show_adv_stats()
				print('\n')

	def flush_hand(self):
		"""
		calls the flush hands function for all the players
		:return:
		"""

		for player in self.players:
			player.flush_hand()

		self.decks_remaining = self.get_remaing_deck()

		self.true_count = self.game_count / (self.get_remaing_deck()+1)
		pass

if __name__ == '__main__':

	
	deck = d.Deck()
	deck.initialize(number_of_card=52, random_order=True)

	player1 = p.Player(player_type = "Gambler", name="Player One")

	game = Game(deck)
	game.add_players(player1)

	for i in range(1):

		game.pass_cards(2)
		game.show_player_stats()

		game.flush_hand()
