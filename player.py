#!/usr/bin/python
from collections import OrderedDict
from cerberus import Validator
import deck as d
import stat as s
from  playstyle import Playstyle

class Player(Playstyle):
	"""
	Class reprenseting a player
	A player havec style class which he inherits
	"""

	__player_type = ['Dealer', 'Gambler']
	__player_Style = ['NoBust', 'CardCounting', 'Standard', 'Custom', 'Dealer']

	def __init__(self, name=[], player_type='Gambler', playstyle='Standard'):
		"""
		Initiate a player.
		:param name: Name of the player will raise execption if null
		:param player_type: Type of player
		:param playstyle:  Playstyle of the player
		"""

		#inherite the function of the playstyle class
		super(Player, self).__init__()

		#data validation
		if name == []:
			# print "One of the necessary arg are empty: Class Player needs a name\n or theres no stats object"
			raise Exception("One of the necessary arg are empty: Class Player needs a name\n \t\t or theres no "
		                    "stats object")

		schema = {'Player Type': {'allowed':self.__player_type}}#,'Stats obj': {'allowed':['stats']}}
		v = Validator(schema)

		if not v.validate({'Player Type': [player_type]}):
			raise Exception(v.errors,"Allowed Type:" +str(self.__player_type))

		if not name:
			print("Player needs a Name/Id")
			raise(TypeError)

		if player_type == 'Dealer':
			self.set_playstyle('Dealer')
		else:
			self.set_playstyle(playstyle)

		#Player variables
		self.name = name
		self.type = player_type
		self.number_of_card = 0
		self.cards = []

		self.victory = 0
		self.loss = 0
		self.requested_stat=0
		self.money = 100
		self.betting_size = 10
		self.pbet = 0

		#special case with aces in the game of blackjack
		self.has_aces = False
		self.number_of_aces = 0

	def hit(self, deck):
		"""
		Give the player a new card from the deck
		:param deck: a deck class with which the game is played with
		:return: NA
		"""

		if not isinstance(deck, d.Deck):
			print("Function take Deck Class as Input")
			return None
		try:
			card = deck.deck.pop()
		except IndexError:
			print("Deck is empty!!!")
			return None

		#Exception for aces
		if card.number == 'a':
			self.has_aces = True
			self.number_of_aces += 1

		#get the card from the deck
		self.cards.append(card)
		self.number_of_card += 1

		self.calculate_total()

	def play(self, deck, *arg):
		"""
		This function hit cards according to the playerstyle
		:param deck: A deck of card of class Deck
		:param arg: arguments for the player according to his style to take a decision
		:return: NA
		"""

		if self.total == []:
			self.hit(deck)

		# will ask for cards until logid returns FALSE
		while self.logic(*arg):
			self.hit(deck)

	def calculate_total(self):
		"""
		This function calculate the sum of the card. Special case with aces
		:return:  NA
		"""

		local_total = 0

		for card in self.cards:

			conv = card.conversion()
			local_total = local_total + conv

		# If you have aces, you actually have 2 possible value
		if self.has_aces:
			self.total = [local_total - self.number_of_aces*10 , local_total - self.number_of_aces*10 + 10]

		else:
			self.total = [local_total]

	def bet(self, amount = 0):
		"""
		The betting function. Adjust the total money the player have. Adjust the bet according to playstyle
		:param amount:
		:return:
		"""

		if amount is 0:
			self.money -=  self.betting_size * (self.requested_stat +1)
			self.pbet = self.betting_size * (self.requested_stat +1)

		else:
			self.money - amount
			self.pbet = amount

	def request_game_stats(self, stat):
		"""
		According to the playstyle of the player, he will request the game object for a stats in order to ajdust
		his betting.
		:param stat: Game Stat object
		:return:
		"""

		# TODO other style, now its only nobust
		if self.playstyle is "NoBust":
			self.requested_stat = stat.give_stats_to_player("Bust_Slope")

	def show_stats(self):
		"""
		Show player stats
		:return:
		"""

		stats_tab = OrderedDict([
					 ('Name', self.name),
					 #('Player Type' , self.type),
					 #('Stand On', self.stand_on),
					 ('Total', self.total),
					 #('Has Busted', self.has_busted),
					 #('Number of Cards', self.number_of_card),
					])

		for stats, number in stats_tab.items():
			print ("{0} ==> {1}".format(stats, number))

		print("Cards:")
		if not self.cards:
			print ("The %s has no card" % self.name)

		for card in self.cards:
			card.show()

		print("\n")

	def show_adv_stats(self):
		"""
		Show advanced player stats such as what he stands on, number of time he has busted, etc.
		:return: NA
		"""

		stats_tab = OrderedDict([
					 ('Name', self.name),
					 ('Player Type' , self.type),
					 ('Play Style', self.playstyle),
					 ('Stand On', self.stand_on),
					 ('Total', self.total),
					 ('Has Busted', self.has_busted),
					 ('Number of Cards', self.number_of_card),
					 ('victory',self.victory),
					 ('Loss', self.loss),
					 ('Money',self.money)
					])

		for stats,number in stats_tab.items():
			print ('{0:17} ==> {1:12}'.format(stats, number))


	def flush_hand(self):
		"""
		Flushing the hand. Putting everything to default value
		:return: NA
		"""

		self.number_of_card = 0
		self.cards = []
		self.total = []
		self.has_aces = False
		self.number_of_aces = 0
		self.has_busted = False


if __name__ == '__main__':
	import stats as s
	import game as g
	
	deck = d.Deck()
	deck.initialize(number_of_card=52,random_order=True)
	game = g.Game(deck)

	stat = s.Stats(game)

	player1 = Player(name="Roddrigo",player_type = "Dealer")

	player1.hit(deck)
	
	player1.play(deck)

	player1.bet()
	print (player1.pbet)
	player1.show_stats()


