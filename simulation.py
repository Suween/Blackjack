
import game as g
import deck as d
import player as p

if __name__ == '__main__':

	############ Intit ###############
	# --> Create Deck, Add players   #
	# --> start the game             #
	##################################

	print("Creating Deck")
	deck = d.Deck()
	number_of_card = 50 * 52
	deck.initialize(number_of_card=number_of_card, random_order=True)

	game = g.Game(deck)

	player1 = p.Player(player_type="Gambler", name="Player One", playstyle='NoLogic')
	player2 = p.Player(player_type="Gambler", name="Player Two", playstyle='NoBust')
	player3 = p.Player(player_type="Gambler", name="Player Three", playstyle='Standard')

	print("Creating Game & players")

	game.add_players(player1, player2, player3)
	game.add_stats_obj()

	Is_deck_empty = False

	Game_played = 0


	############ Round ###############
	# --> Pass 2 card to each Player #
	##################################
	print ("Simulation started")
	for z in range(100):
		Is_deck_empty = game.pass_cards(2)

		if Is_deck_empty:

			game.place_bets()

			# play_round() is where the player decide if he takes a card or not.
			# He will follow the rules of the given "stand_on" parameter.
			# By default, the player stand on 12 and the dealer on 17
			game.play_round('Gambler', deck)

			game.play_round('Dealer', deck)
				
			#compare() is where the player compare thier hand with the dealer's and check who won the hand.
			game.compare()

			game.stats.update_stats()
		else:
			break

		game.flush_hand()
		game.give_stats_to_players()

	# game.stats.show_all(['wins', "bet_size", 'money'])
	game.stats.show_all(['count'])

