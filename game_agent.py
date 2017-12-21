"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    #print("score called with legal moves {}".format(game.get_legal_moves(player)))
    return float(len(game.get_legal_moves(player))) # my-moves heuristic (for now)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return float(len(game.get_legal_moves(player)) - len(game.get_legal_moves(game.get_opponent(player))))


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return float(len(game.get_legal_moves(player)) - 2*len(game.get_legal_moves(game.get_opponent(player))))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
        
    def max_value(self, game, depth, searching_player):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Check if state terminal and return value if so
        v = game.utility(searching_player)
        if v:
            return v
        if depth==0:
            return self.score(game, searching_player)
        # Else return max of child nodes, remembering to decrement depth in call
        return max(self.min_value(game.forecast_move(move), depth-1, searching_player) for \
                   move in game.get_legal_moves())
        

    def min_value(self, game, depth, searching_player):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # Check if state terminal and return value if so
        v = game.utility(searching_player)
        if v:
            return v
        if depth==0:
            return self.score(game, searching_player)
        # Else return max of child nodes, remembering to decrement depth in call
        return min(self.max_value(game.forecast_move(move), depth-1, searching_player) for \
                   move in game.get_legal_moves())


    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # TODO: finish this function!
        # Check that depth is at least one (not meaningful to call this function otherwise)
        # Also return if no legal moves available
        if depth==0 or not game.get_legal_moves():
            return (-1, -1)

        # Print depth 1 values (for debugging)
        #print("Minimax player -- scores for next actions:")
        #for move in game.get_legal_moves():
        #    print(move, self.min_value(game.forecast_move(move), depth-1, game.active_player))
        
        # Else run minimax, remember to decrement depth in call to min_value
        return max(game.get_legal_moves(), \
                   key=lambda move: self.min_value(game.forecast_move(move), depth-1, game.active_player))



class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        best_move = (-1, -1)
        self._value_of_last_move_returned = float("-inf")
        current_depth = 1
        optimum_strategy_found = False

        try:
            while self._value_of_last_move_returned != float("inf"): # i.e. break loop if optimal strategy found
                best_move = self.alphabeta(game, current_depth, float("-inf"), float("inf"))
                current_depth += 1
        except SearchTimeout:
            #print("Timed out at depth {}".format(current_depth))
            pass

        return best_move
        
    def max_value(self, game, depth, searching_player, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Terminal test
        v = game.utility(searching_player)
        if v:
            return v
        if depth==0:
            return self.score(game, searching_player)
        # Alpha-beta max-min
        v = float("-inf")
        for move in game.get_legal_moves():
            v = max(v, self.min_value(game.forecast_move(move), depth-1, searching_player, alpha, beta))
            if v>=beta:
                return v
            alpha = max(alpha, v)
        return v
        

    def min_value(self, game, depth, searching_player, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Terminal test
        v = game.utility(searching_player)
        if v:
            return v
        if depth==0:
            return self.score(game, searching_player)
        # Alpha-beta min-max
        v = float("inf")
        for move in game.get_legal_moves():
            v = min(v, self.max_value(game.forecast_move(move), depth-1, searching_player, alpha, beta))
            if v<=alpha:
                return v
            beta = min(beta, v)
        return v

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!
        # Check that depth is at least one (not meaningful to call this function otherwise)
        # Also return if no legal moves available
        if depth==0 or not game.get_legal_moves():
            return (-1, -1)
        
        # Else run minimax, remember to decrement depth in call to min_value
        # This one returns an alpha-beta pruned version of the argmax
        v = float("-inf")
        best_move = game.get_legal_moves()[0] # Default move if all actions are infinitely poor
        #print("AlphaBeta player -- scores for next actions:")
        for move in game.get_legal_moves():
            trial_v = self.min_value(game.forecast_move(move), depth-1, game.active_player, alpha, beta)
            # Print depth 1 values (for debugging)
            #print(move, trial_v)

            if trial_v > v:
                v = trial_v
                best_move = move
            # Don't need to check if v>=beta as it will never happen at root node (beta == inf)
            alpha = max(alpha, v)

        # A hack, but I can't change the interface for this function without failing the unit
        # tests :-(
        self._value_of_last_move_returned = v 
        
        return best_move

