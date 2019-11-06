#!/usr/bin/python
from cerberus import Validator

class Playstyle(object):


	def __init__(self):

		self.player_Style = ['NoBust','CardCounting','Standard','Custom','Dealer','NoLogic']
		self.playstyle = None

		self.total = []
		self.standard_stand_on= 17
		self.NoBust_Stand_on = 12
		self.dealer_stand_on = 17

		self.stand_on = 0

		self.has_busted = False
		self.bust_count = 0
		self.no_bust_upper_limit = self.dealer_stand_on

		self.function_dict = {
		  'NoBust': self.no_bust_logic,
		  'Standard': self.standard_logic,
		  'CardCounting': self.cardcount_logic,
		  'Dealer': self.dealer_logic,
		  'NoLogic' : self.dealer_logic
		}

	def set_playstyle(self,playstyle):

		schema = {'Player style': {'allowed':self.player_Style}}#,'Stats obj': {'allowed':['stats']}}
		v = Validator(schema)

		if not v.validate({'Player style': [playstyle]}):
			raise Exception(v.errors,"Allowed Type:" +str(self.player_Style))

		self.playstyle = playstyle

	def logic(self,*arg):
		return self.function_dict[self.playstyle](*arg)

	def no_bust_logic(self,*arg):

		self.stand_on = self.NoBust_Stand_on

		if (21 >= min(self.total) >= self.no_bust_upper_limit) or (21 >= max(self.total) >= self.no_bust_upper_limit):
			return False

		elif min(self.total) >= self.NoBust_Stand_on:
			return False
		else:
			return True

	def standard_logic(self,arg):

		dealer = next((x for x in arg if x.type == 'Dealer'), None)

		dealer_reavealed_card = dealer.cards[1].conversion()

		if max(self.total) < 11:

			return True
			pass

		if max(self.total) == 12 or min(self.total) ==12:

			if  6 >= dealer_reavealed_card >= 4: 

				return False
				pass

		if 13 <= max(self.total) <= 16 or 13 <= min(self.total) <= 16:

			if 6 >= dealer_reavealed_card:

				return False
				pass

		if max(self.total) >= 17 or min(self.total) >= 17:

			return False
			pass

		return True

	def cardcount_logic(self,*arg):
		print ("cardcounting")

	def dealer_logic(self,*arg):
		self.stand_on = self.dealer_stand_on
		
		if (21 >= min(self.total) >= self.dealer_stand_on) or (21 >= max(self.total) >= self.dealer_stand_on):

			return False

		elif not(min(self.total) > self.dealer_stand_on or max(self.total) > self.dealer_stand_on):

			return True

		elif min(self.total) < self.dealer_stand_on and max(self.total) > 21:
			
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

