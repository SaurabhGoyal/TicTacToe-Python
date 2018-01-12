class Game:

    # Represents a blank cell
    BLANK_CELL_CHAR = '_'
    # To benchmark how-many times execution goes to leaf.
    LEAF_COUNT = 0

    def __init__(self, *args, **kwargs):

        # Actual board state
        self.board = {pos: self.BLANK_CELL_CHAR for pos in ['00', '01', '02', '10', '11', '12', '20', '21', '22']}

        # Map for storing winner of each game state.
        self.available_moves = set(self.board.keys())

        # Characters for both types of players.
        self.human = kwargs.get('human', 'x')
        self.comp = 'o' if self.human == 'x' else 'x'

        # Map for caching winner of each game state.
        self.state_winner_map = {self.BLANK_CELL_CHAR * 9: None}

        # Map for caching best move and score for each game state.
        self.state_best_move_map = {self.BLANK_CELL_CHAR * 9: {self.comp: ('02', 0)}}

    def _all_elem_same(self, row):
        """ Returns if all elements in given list are same and not blank """
        return len(set(row)) == 1 and row[0] != self.BLANK_CELL_CHAR

    def get_board_state(self):
        """ Returns serialized game state to be used for caching """

        board_state = ''
        for i in range(0, 3):
            board_state += ''.join([self.board['{}{}'.format(i, j)] for j in range(0, 3)])
        return board_state

    def get_board_state_pretty(self):
        """ Returns game board state in pretty format to be used by game-managers """

        board_state = ''
        for i in range(0, 3):
            board_state += ' | '.join([self.board['{}{}'.format(i, j)] for j in range(0, 3)])
            board_state += '\n'
        return board_state

    def get_winner(self):
        """
        Returns winner in current game state.
        """
        
        current_board_state = self.get_board_state()
        current_board_state_winner = self.state_winner_map.get(current_board_state)
        if current_board_state_winner:
            return current_board_state_winner

        # At-least 5 moves must have been played for a possible win.
        if len(self.available_moves) > 4:
            return None

        winner = None

        for i in range(0, 3):
            row = [self.board['{}{}'.format(i, j)] for j in range(0, 3)]
            if self._all_elem_same(row):
                winner = row[0]
                break

        if not winner:
            for i in range(0, 3):
                row = [self.board['{}{}'.format(j, i)] for j in range(0, 3)]
                if self._all_elem_same(row):
                    winner = row[0]
                    break

        if not winner:
            row = [self.board['{}{}'.format(i, i)] for i in range(0, 3)]
            if self._all_elem_same(row):
                winner = row[0]

        if not winner:
            row = [self.board['{}{}'.format(2-i, i)] for i in range(0, 3)]
            if self._all_elem_same(row):
                winner = row[0]

        self.state_winner_map[current_board_state] = winner
        return winner

    def get_best_move(self, curr_player, orig_player, depth=0, alpha=-100, beta=100):
        """
        Returns a tuple consisting of the best move along-with the best score for current player
        in current game state
        """

        best_move, best_score = None, 0
        is_over, winner = self.is_over()

        current_board_state = self.get_board_state()
        current_board_state_best_move_score = self.state_best_move_map.get(current_board_state, {}).get(curr_player)

        if current_board_state_best_move_score:
            return current_board_state_best_move_score

        # If game is over return the score
        if is_over:
            self.LEAF_COUNT += 1
            if winner:
                best_score = (10 - depth) * (1 if winner == orig_player else -1)
            return best_move, best_score

        opponent = self.human if curr_player == self.comp else self.comp

        # Else find the move with best score.
        for move in list(self.available_moves):

            self.play_move(move, curr_player)
            _, score = self.get_best_move(opponent, orig_player, depth=depth+1, alpha=alpha, beta=beta)

            # If move is for orig-player, max score move will be best move.
            if best_move is None or (curr_player == orig_player and score > best_score):
                best_move, best_score = move, score
                alpha = max(alpha, best_score)
            # If move is not for orig-player, min score move will be best move.
            elif best_move is None or (curr_player != orig_player and score < best_score):
                best_move, best_score = move, score
                beta = min(beta, best_score)

            self.undo_move(move)

            # If the maximum harm (-ve score) the opponent can do is less than the minimum benefit (+ve score) the
            # current player has, no need to check other moves as the opponent can not do better.
            if beta <= alpha:
                break

        self.state_best_move_map[current_board_state] = self.state_best_move_map.get(current_board_state) or {}
        self.state_best_move_map[current_board_state][curr_player] = best_move, best_score
        return best_move, best_score

    def play_move(self, move, player):
        """ Validates and makes the given move for given player """
        if move in self.available_moves:
            self.available_moves.remove(move)
            self.board[move] = player
        else:
            raise ValueError('Move [{} - {}] not possible.'.format(move, player))

    def undo_move(self, move):
        """ Validates and undoes the given move """
        if move in self.board:
            self.board[move] = self.BLANK_CELL_CHAR
            self.available_moves.add(move)
        else:
            raise ValueError('Move-undo [{}] not possible.'.format(move))

    def is_over(self):
        """
        Returns tuple consisting of flag represneting whether games is over along-with the winner of the game if any
        """
        winner = self.get_winner()
        status = bool(winner or not self.available_moves)
        return status, winner
