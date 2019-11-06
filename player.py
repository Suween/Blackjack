#!/usr/bin/python
from collections import OrderedDict
from cerberus import Validator
import deck as d
import stat as s
from  playstyle import Playstyle

class Player(Playstyle):

	__player_type = ['Dealer','Gambler']
	__player_Style = ['NoBust','CardCounting','Standard','Custom','Dealer']


	def __init__(self, name=[], player_type='Gambler',playstyle='Standard'):#,stats=[]):

		super(Player,self).__init__()

		if name == []:# or stats == []:
			# print "One of the necessary arg are empty: Class Player needs a name\n or theres no stats object"
			raise Exception("One of the necessary arg are empty: Class Player needs a name\n \t\t or theres no stats object")


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

		self.name = name
		self.type = player_type

		self.number_of_card = 0
		self.cards = []
		self.has_aces = False
		self.number_of_aces = 0

		self.victory = 0
		self.loss = 0

		self.requested_stat=0

		self.money = 100
		self.betting_size = 10
		self.pbet = 0 

	def hit(self,deck):

		if not isinstance(deck, d.Deck):
			print("Function take Deck Class as Input")
			return None
		try:
			card = deck.deck.pop()
		except IndexError:
			print("Deck is empty!!!")
			#pass
			raise

		if card.number == 'a':
			self.has_aces = True
			self.number_of_aces += 1


		self.cards.append(card)
		self.number_of_card += 1
		
		self.calculate_total()

		
	def play(self,deck,*arg):

		if self.total == []:
			self.hit(deck)

		while self.logic(*arg):
			self.hit(deck)

	def calculate_total(self):

		local_total = 0

		for card in self.cards:

			conv = card.conversion()
			local_total = local_total + conv

		if self.has_aces:
			self.total = [local_total - self.number_of_aces*10 ,local_total - self.number_of_aces*10 + 10]

		else:
			self.total = [local_total]


	def bet(self, amount = 0):

		if amount is 0:
			self.money -=  self.betting_size * (self.requested_stat +1)
			self.pbet = self.betting_size * (self.requested_stat +1)

		else:
			self.money - amount
			self.pbet = amount

	def request_game_stats(self,stat):

		if self.playstyle is "NoBust":
			self.requested_stat = stat.give_stats_to_player("Bust_Slope")


	def show_stats(self):

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
			print ('{0:17} ==> {1:>12}'.format(stats, number))


	def flush_hand(self):

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


