#!/usr/bin/python

import random
from cerberus import Validator

class Card:

	__color_choice = ['D', 'C', 'H', 'S']
	__number_choice = ['a','2','3','4','5','6','7','8','9','10','J','Q','K']

	def __init__(self):

		self.number = []
		self.color = []
		
	def random(self):
		 
		 self.number = random.choice(self.__number_choice)
		 self.color = random.choice(self.__color_choice)

	def create_card(self,number,color):

		schema = {'color': {'allowed':self.__color_choice},
				  'number':{'allowed':self.__number_choice}}
		v = Validator(schema)

		if not v.validate({'color': [color],'number': [number]}):
			print(v.errors)
			print("Allowed Number:" +str(self.__number_choice))
			print("Allowed Color:" +str(self.__color_choice))

		self.number = number
		self.color = color

	def show(self):
		print(self.number,self.color)

	def conversion(self):

		if self.number in {'J','Q','K'}:
			return 10
		elif self.number == 'a':
			return 11
		else:
			return int(self.number)

class Deck:

	def __init__(self):#, number_of_card):

		self.deck_size = []
		self.deck = []

	def initialize(self,number_of_card=52,random_cards=False, random_order = False):

		self.deck = [Card() for i in range(number_of_card)]
		self.deck_size = number_of_card

		count = 0
		done = True

		if random_cards:
			for card in self.deck:
				card.random()

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

		for card in self.deck:
			card.show()

	def shuffle(self,iteration=3):

		# count = 0
		# validate = [None] * self.deck_size

		# for card in self.deck:

		# 	validate[count] = not((isinstance(card, Card) and (card.color != [] or card.number != [])))
		# 	count += 1

		# if any(validate):
		# 	print("Not all instances of the decks are cards OR Some cards are empty")

		for i in range(iteration):
			random.shuffle(self.deck)



if __name__ == '__main__':

	# card = Card()
	# card.random()
	# print(card.number, card.color)

	# card.create_card('A','D')
	# print(card.number, card.color)

	deck = Deck()
	deck.initialize(number_of_card=52,random_order=True)#,random_cards = True)

	deck.show_deck()



