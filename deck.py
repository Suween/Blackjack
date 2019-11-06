"""
Author : Vincent Tanguay Casgrain
Date: 2017-08-09
"""

import random
from cerberus import Validator

class Card:
	"""
	Card Class

	This class represent 1 card of the deck
	@create_card to create a card
	"""

	__color_choice = ['D', 'C', 'H', 'S']
	__number_choice = ['a','2','3','4','5','6','7','8','9','10','J','Q','K']

	def __init__(self):

		self.number = []
		self.color = []
		
	def random(self):
		"""
		Chose a random color and a random number from the color and number choices
		"""
		 
		self.number = random.choice(self.__number_choice)
		self.color = random.choice(self.__color_choice)

	def create_card(self, number, color):
		"""
		create a card
		:param number: The number of the card
		:param color: The color of the card
		:return:
		"""

		#Validating inputs
		schema = {'color': {'allowed':self.__color_choice},
				  'number':{'allowed':self.__number_choice}}
		v = Validator(schema)

		if not v.validate({'color': [color],'number': [number]}):
			print(v.errors)
			print("Allowed Number:" + str(self.__number_choice))
			print("Allowed Color:" + str(self.__color_choice))
			raise(ValueError)

		self.number = number
		self.color = color

	def show(self):
		print(self.number, self.color)

	def conversion(self):
		"""
		Converts the faces to number to be mathematically usable
		:return: The blackjack value of the face
		"""

		if self.number in {'J','Q','K'}:
			return 10
		elif self.number == 'a':
			return 11
		else:
			return int(self.number)

class Deck:
	"""
	Deck Class
	The deck is actually a deck of card.
	Comes with the methods or action you can do on a deck like Shuffle

	Takes no arguments
	"""

	def __init__(self):

		self.deck_size = []
		self.deck = []

	def initialize(self, number_of_card = 52, random_cards = False, random_order = False):
		"""
		initialise the deck card
		:param number_of_card: How many card you want in the deck
		:param random_cards: False for the card to be created senquetially, False to create them randomly
		:param random_order: False to output the deck sequentially, True to shuffle the deck (random order)
		:return: A deck of card (list of card objects)
		"""

		#empty array of size of the deck
		self.deck = [Card() for i in range(number_of_card)]
		self.deck_size = number_of_card

		count = 0
		done = True

		#if game has choosen a completly random set of cards
		if random_cards:
			for card in self.deck:
				card.random()

		#if the game want something close to a real decks
		#these loops will create [ad, 2d, 3d... JS, QS, KS] until number of card condition is meet
		else:
			while done:
				for color in ['D', 'C', 'H', 'S']:
					for number in ['a','2','3','4','5','6','7','8','9','10','J','Q','K']:
					
						if count < self.deck_size:
							self.deck[count].create_card(number,color)
						else:
							done = False
							break

						count += 1
		if random_order:
			self.shuffle()


	def show_deck(self):
		"""
		Print the deck in the console
		Calls the card show function
		:return:
		"""

		for card in self.deck:
			card.show()

	def shuffle(self, iteration=3):
		"""
		Shuffle the deck with random library
		:param iteration: Number of time you want to shuffle your deck
		"""
		for i in range(iteration):
			random.shuffle(self.deck)

if __name__ == '__main__':

	deck = Deck()
	deck.initialize(number_of_card=52,random_order=True)#,random_cards = True)

	deck.show_deck()



