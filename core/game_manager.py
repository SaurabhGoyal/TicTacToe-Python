


class GameManager:
    """ A class to manage a TicTacToe game """

    def __init__(self, *args, **kwargs):
        self.game = None

    def start_game(self, **kwargs):
        """ starts a new game """
        self.game = Game(player=kwargs.get('player', 'x'))
        if input('Would you like to go first? y/n\n') == 'y':
            self.play_human_move()
        else:
            self.play_comp_move()

    def play_comp_move(self):
        """ Plays computer move and decides further """
        print('Comp thinking...')
        self.game.LEAF_COUNT = 0
        self.game.play_move(self.game.get_best_move(self.game.comp, self.game.comp, 0)[0], self.game.comp)
        print('Called leaf {} times.'.format(self.game.LEAF_COUNT))
        self.check_status(self.game.human)

    def play_human_move(self, error=''):
        """ Takes input from user and plays human move and decides further """
        print('{}Make your next move...'.format(error))
        move = str(input())
        try:
            self.game.play_move(move, self.game.human)
        except ValueError:
            self.play_human_move('Invalid move - ')
        self.check_status(self.game.comp)

    def check_status(self, next_player):
        """ Check what should be done after a move and proceeds accordingly """
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
