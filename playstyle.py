#!/usr/bin/python
from cerberus import Validator
import csv

class Playstyle(object):


	def __init__(self):

		self.player_Style = ['NoBust','CardCounting','Standard','Custom','Dealer','NoLogic']
		self.playstyle = None

		self.total = []
		self.number_of_card = 0

		self.stand_on = 0

		self.DEFAULT_SIZE = 10

		self.has_busted = False
		self.bust_count = 0

		self.pbet = 0

		self.standard_table_logic = []

		self.function_dict = {
			'NoBust': self.no_bust_logic,
			'Standard': self.standard_logic,
			'CardCounting': self.cardcount_logic,
			'Dealer': self.dealer_logic,
			'NoLogic' : self.dealer_logic
		}

	def set_playstyle(self, playstyle):

		schema = {'Player style': {'allowed':self.player_Style}}
		v = Validator(schema)

		if not v.validate({'Player style': [playstyle]}):
			raise Exception(v.errors, "Allowed Type:" + str(self.player_Style))

		self.playstyle = playstyle

		if self.playstyle == 'Standard':
			with open('logic/standard.csv') as  csvfile :
				[self.standard_table_logic.append(row) for row in csv.reader(csvfile, delimiter=',')]

	def logic(self, *arg):
		return self.function_dict[self.playstyle](*arg)

	def no_bust_logic(self, *arg):

		self.stand_on = 12
		DEALER_LIMIT = 17

		if (21 >= min(self.total) >= DEALER_LIMIT) or (21 >= max(self.total) >= DEALER_LIMIT):
			return False

		elif min(self.total) >= self.stand_on:
			return False
		else:
			return True

	def standard_logic(self, arg):

		action = ""

		dealer = next((x for x in arg if x.type == 'Dealer'), None)
		dealer_reavealed_card = dealer.cards[1].conversion()

		if min(self.total) >= 21 or max(self.total) >= 21:
			self.has_busted = True
			return False

		idx = self.standard_table_logic[0].index(str(dealer_reavealed_card))

		for row in self.standard_table_logic:
			if row[0] == str(min(self.total)) or row[0] == str(max(self.total)):
				action = row[idx]

		if action == 's':
			return False
		elif action == 'h':
			return True
		elif action == 'd':
			if self.number_of_card <= 2:
				self.pbet += self.pbet
		else:
			raise(TypeError("Unknown value in standard logic table"))

			return True

	def cardcount_logic(self,*arg):
		print ("cardcounting")

	def dealer_logic(self, *arg):

		self.stand_on = 17
		
		if (21 >= min(self.total) >= self.stand_on) or (21 >= max(self.total) >= self.stand_on):

			return False

		elif not(min(self.total) > self.stand_on or max(self.total) > self.stand_on):

			return True

		elif min(self.total) < self.stand_on and max(self.total) > 21:
			
			return True

		elif min(self.total) >= 21 or max(self.total) >= 21:

			self.has_busted = True

			return False
		else:
			print("wth")
			print(self.total)

if __name__ == '__main__':

	p = Playstyle()
	p.set_playstyle('Standard')

	# p.logic()

