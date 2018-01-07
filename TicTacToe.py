class Game:

    # Represents a blank cell
    BLANK_CELL_CHAR = ' '
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
        return len(set(row)) == 1 and row[0] != self.BLANK_CELL_CHAR

    def get_board_state(self):

        board_state = ''
        for i in range(0, 3):
            board_state += ''.join([self.board['{}{}'.format(i, j)] for j in range(0, 3)])
        return board_state

    def get_board_state_pretty(self):

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

        best_move, best_score = None, 0
        is_over, winner = self.is_over()

        current_board_state = self.get_board_state()
        current_board_state_best_move_score = self.state_best_move_map.get(current_board_state, {}).get(curr_player)

        if current_board_state_best_move_score:
            return current_board_state_best_move_score

        if is_over:
            self.LEAF_COUNT += 1
            if winner:
                best_score = (10 - depth) * (1 if winner == orig_player else -1)
            return best_move, best_score

        opponent = self.human if curr_player == self.comp else self.comp

        for move in list(self.available_moves):

            self.play_move(move, curr_player)
            _, score = self.get_best_move(opponent, orig_player, depth=depth+1, alpha=alpha, beta=beta)

            if best_move is None or (curr_player == orig_player and score > best_score):
                best_move, best_score = move, score
                alpha = max(alpha, best_score)
            elif best_move is None or (curr_player != orig_player and score < best_score):
                best_move, best_score = move, score
                beta = min(beta, best_score)

            self.undo_move(move)

            if beta <= alpha:
                break

        self.state_best_move_map[current_board_state] = self.state_best_move_map.get(current_board_state) or {}
        self.state_best_move_map[current_board_state][curr_player] = best_move, best_score
        return best_move, best_score

    def play_move(self, move, player):
        if move in self.available_moves:
            self.available_moves.remove(move)
            self.board[move] = player
        else:
            raise ValueError('Move [{} - {}] not possible.'.format(move, player))

    def undo_move(self, move):
        if move in self.board:
            self.board[move] = self.BLANK_CELL_CHAR
            self.available_moves.add(move)
        else:
            raise ValueError('Move-undo [{}] not possible.'.format(move))

    def is_over(self):
        winner = self.get_winner()
        status = bool(winner or not self.available_moves)
        return status, winner


class GameManager:

    def __init__(self, *args, **kwargs):
        self.game = None

    def start_game(self, **kwargs):
        self.game = Game(player=kwargs.get('player', 'x'))
        if input('Would you like to go first? y/n\n') == 'y':
            self.play_human_move()
        else:
            self.play_comp_move()

    def play_comp_move(self):
        print('Comp thinking...')
        self.game.LEAF_COUNT = 0
        self.game.play_move(self.game.get_best_move(self.game.comp, self.game.comp, 0)[0], self.game.comp)
        print('Called leaf {} times.'.format(self.game.LEAF_COUNT))
        self.check_status(self.game.human)

    def play_human_move(self, error=''):
        print('{}Make your next move...'.format(error))
        move = str(input())
        try:
            self.game.play_move(move, self.game.human)
        except ValueError:
            self.play_human_move('Invalid move - ')
        self.check_status(self.game.comp)

    def check_status(self, next_player):
        print(self.game.get_board_state_pretty())
        status, winner = self.game.is_over()
        if status:
            if winner:
                if winner == self.game.human:
                    print('Impossible!!! How did you beat me...')
                else:
                    print('You are no match to me...')
            else:
                print('Looks like a draw...')
            if input('Play again?y/n...\n') == 'y':
                self.start_game()
        else:
            if next_player == self.game.comp:
                self.play_comp_move()
            else:
                self.play_human_move()
