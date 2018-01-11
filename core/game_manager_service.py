from core import constants as core_constants
from core.game import Game


class GameManagerService:
    """ A class to manage a TicTacToe game service """

    def __init__(self, *args, **kwargs):
        self.game = None
        self.status = None

    def start_game(self, player, first_turn, **kwargs):
        """ starts a new game """

        success, info = False, {}

        if self.status not in [
            core_constants.GAME_STATUS_OVER_DRAW,
            core_constants.GAME_STATUS_OVER_COMP_WINNER,
            core_constants.GAME_STATUS_OVER_HUMAN_WINNER
        ]:
            info = {
                'error_code': core_constants.ERROR_CODE_GAME_ALREADY_ACTIVE,
                'messages': ['Another game already running']
            }
        else:
            self.game = Game(player=player)
            if first_turn:
                self.status = core_constants.GAME_STATUS_HUMAN_MOVE_REQUIRED
                success, info = True, {
                    'status_code': self.status,
                    'messages': []
                }
            else:
                self.status = core_constants.GAME_STATUS_COMP_MOVE_REQUIRED
                success, info = self._play_comp_move()

        return success, info

    def play_human_move(self, move):
        """ Takes input from user and plays human move and decides further """

        success, info = False, {}

        if self.status != core_constants.GAME_STATUS_HUMAN_MOVE_REQUIRED:
            info = {
                'error_code': core_constants.ERROR_CODE_NOT_PLAYER_TURN,
                'messages': ['It\'s not player\'s turn']
            }

        else:
            try:
                self.game.play_move(move, self.game.human)
                success, info = self._check_status(self.game.comp, {'success': success, 'info': info})
            except ValueError:
                info = {
                    'error_code': core_constants.ERROR_CODE_INVALID_MOVE,
                    'messages': ['Invalid move']
                }

        return success, info

    def _play_comp_move(self):
        """ Plays computer move and decides further """

        self.game.LEAF_COUNT = 0
        self.game.play_move(self.game.get_best_move(self.game.comp, self.game.comp, 0)[0], self.game.comp)
        success, info = True, {
            'status_code': self.status,
            'messages': []
        }
        # print('Called leaf {} times.'.format(self.game.LEAF_COUNT))
        return self._check_status(self.game.human, {'success': True, 'info': info})

    def _check_status(self, next_player):
        """ Check what should be done after a move and proceeds accordingly """

        success, info = True, {}

        status, winner = self.game.is_over()
        if status:
            if winner:
                if winner == self.game.human:
                    self.status = core_constants.GAME_STATUS_OVER_HUMAN_WINNER
                else:
                    self.status = core_constants.GAME_STATUS_OVER_COMP_WINNER
            else:
                self.status = core_constants.GAME_STATUS_OVER_DRAW
        else:
            if next_player == self.game.comp:
                self.status = core_constants.GAME_STATUS_COMP_MOVE_REQUIRED
                success, info = self._play_comp_move()
            else:
                self.status = core_constants.GAME_STATUS_HUMAN_MOVE_REQUIRED

        if not info:
            info = {
                'status_code': self.status
            }

        return success, info
