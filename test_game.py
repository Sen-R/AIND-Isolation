from game_agent import *
from sample_players import GreedyPlayer

from isolation import Board

player1 = AlphaBetaPlayer()
player2 = AlphaBetaPlayer()
player1.search_depth = 14
player2.search_depth = 5
player1.score = custom_score_3
player2.score = custom_score_2

game = Board(player1, player2, 7,7)
game._board_state[5] = 1

print("\nInitial board:")
print(game.to_string())

print(game.play( time_limit=500))
print("Player 1: {}".format(player1))
print("Player 2: {}".format(player2))

#while not game.utility(game.active_player):
#    move1 = player1.get_move(game, lambda:10000)
#    print("\n Chosen move for p1: {}".format(move1))
#    game.apply_move(move1)
#    move2 = player2.get_move(game, lambda:10000)
#    print("\n Chosen move for p2: {}".format(move2))
#    game.apply_move(move2)
#    print("\n Board now:\n{}".format(game.to_string()))
