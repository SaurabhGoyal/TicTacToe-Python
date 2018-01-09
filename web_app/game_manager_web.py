from core.game import Game


class GameManagerWeb:
    """ A class to manage a TicTacToe game on web """

    GAME_STATUS_INIT = 0
    GAME_STATUS_HUMAN_MOVE_REQUIRED = 1
    GAME_STATUS_COMP_MOVE_REQUIRED = 2
    GAME_STATUS_OVER_DRAW = 3
    GAME_STATUS_OVER_HUMAN_WINNER = 4
    GAME_STATUS_OVER_COMP_WINNER = 5

    def __init__(self, *args, **kwargs):
        self.game = None
        self.status = self.GAME_STATUS_INIT

    def start_game(self, player, first_turn, **kwargs):
        """ starts a new game """
        self.game = Game(player=player)
        if first_turn:
            self.status = self.GAME_STATUS_HUMAN_MOVE_REQUIRED
            return self.check_status(self.game.human, {'status': True, 'info': ''})
        else:
            self.status = self.GAME_STATUS_COMP_MOVE_REQUIRED
            return self._play_comp_move()

    def _play_comp_move(self):
        """ Plays computer move and decides further """
        self.game.LEAF_COUNT = 0
        self.game.play_move(self.game.get_best_move(self.game.comp, self.game.comp, 0)[0], self.game.comp)
        # print('Called leaf {} times.'.format(self.game.LEAF_COUNT))
        return self.check_status(self.game.human, {'status': True, 'info': ''})

    def play_human_move(self, move):
        """ Takes input from user and plays human move and decides further """
        move_status, info = False, ''
        try:
            self.game.play_move(move, self.game.human)
            move_status = True
        except ValueError:
            info = 'Invalid move'
        return self.check_status(self.game.comp, {'status': move_status, 'info': info})

    def check_status(self, next_player, prev_move_data):
        """ Check what should be done after a move and proceeds accordingly """

        res_status = 200
        if prev_move_data['status']:
            messages = [self.game.get_board_state_pretty()]
            status, winner = self.game.is_over()
            if status:
                if winner:
                    if winner == self.game.human:
                        self.status = self.GAME_STATUS_OVER_HUMAN_WINNER
                    else:
                        self.status = self.GAME_STATUS_OVER_COMP_WINNER
                else:
                    self.status = self.GAME_STATUS_OVER_DRAW
            else:
                if next_player == self.game.comp:
                    self.status = self.GAME_STATUS_COMP_MOVE_REQUIRED
                    return self._play_comp_move()
                else:
                    self.status = self.GAME_STATUS_HUMAN_MOVE_REQUIRED
        else:
            res_status = 400
            messages = [prev_move_data['info']]

        return res_status, {'game_status': self.status, 'messages': messages}
