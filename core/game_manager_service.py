from core import constants as core_constants
from core.game import Game


class GameManagerService:
    """ A class to manage a TicTacToe game service """

    move_display_value_map = {
        '00': 'top left',
        '01': 'top',
        '02': 'top right',
        '10': 'left',
        '11': 'centre',
        '12': 'right',
        '20': 'lower left',
        '21': 'bottom',
        '22': 'lower right',
    }

    status_code_message_map = {
        core_constants.GAME_STATUS_INIT: 'Game is initializing',
        core_constants.GAME_STATUS_HUMAN_MOVE_REQUIRED: 'Make your move',
        core_constants.GAME_STATUS_COMP_MOVE_REQUIRED: 'Computer is thinking',
        core_constants.GAME_STATUS_OVER_DRAW: 'Looks like a draw',
        core_constants.GAME_STATUS_OVER_HUMAN_WINNER: 'Impossible! How did you beat me',
        core_constants.GAME_STATUS_OVER_COMP_WINNER: 'You are no match to me',
    }

    error_code_message_map = {
        core_constants.ERROR_CODE_GAME_ALREADY_ACTIVE: 'Game is already running',
        core_constants.ERROR_CODE_GAME_OVER: 'Game is over.',
        core_constants.ERROR_CODE_NOT_PLAYER_TURN: 'It\'s not player\'s turn',
        core_constants.ERROR_CODE_INVALID_MOVE: 'Invalid move'
    }

    def __init__(self, *args, **kwargs):
        self.game = None
        self.status = None
        self.last_comp_move = None

    def get_game_status_message(self):
        return self.status_code_message_map[self.status]

    @classmethod
    def get_move_display_text(cls, move):
        return cls.move_display_value_map.get(move)

    def get_last_comp_move_display_text(self):
        return self.get_move_display_text(self.last_comp_move)

    def start_game(self, player, first_turn, **kwargs):
        """ starts a new game """

        success, info = False, {}

        if self.status and self.status not in [
            core_constants.GAME_STATUS_OVER_DRAW,
            core_constants.GAME_STATUS_OVER_COMP_WINNER,
            core_constants.GAME_STATUS_OVER_HUMAN_WINNER
        ]:
            info = {
                'error_code': core_constants.ERROR_CODE_GAME_ALREADY_ACTIVE,
                'messages': [self.error_code_message_map[core_constants.ERROR_CODE_GAME_ALREADY_ACTIVE]]
            }
        else:
            self.game = Game(player=player)
            if first_turn:
                self.status = core_constants.GAME_STATUS_HUMAN_MOVE_REQUIRED
                success, info = True, {
                    'status_code': self.status,
                    'messages': [self.status_code_message_map[self.status]]
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
                'messages': [
                    self.error_code_message_map[
                        core_constants.ERROR_CODE_GAME_OVER
                        if self.status in [
                            core_constants.GAME_STATUS_OVER_DRAW,
                            core_constants.GAME_STATUS_OVER_COMP_WINNER,
                            core_constants.GAME_STATUS_OVER_HUMAN_WINNER
                        ] else core_constants.ERROR_CODE_NOT_PLAYER_TURN
                    ]
                ]
            }

        else:
            try:
                self.game.play_move(move, self.game.human)
                success, info = self._check_status(self.game.comp)
            except ValueError:
                info = {
                    'error_code': core_constants.ERROR_CODE_INVALID_MOVE,
                    'messages': [self.error_code_message_map[core_constants.ERROR_CODE_INVALID_MOVE]]
                }

        return success, info

    def _play_comp_move(self):
        """ Plays computer move and decides further """

        self.game.LEAF_COUNT = 0
        best_move = self.game.get_best_move(self.game.comp, self.game.comp, 0)[0]
        self.game.play_move(best_move, self.game.comp)
        self.last_comp_move = best_move
        success, info = True, {
            'status_code': self.status,
            'messages': []
        }
        # print('Called leaf {} times.'.format(self.game.LEAF_COUNT))
        return self._check_status(self.game.human)

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
                'status_code': self.status,
                'messages': [self.status_code_message_map[self.status]]
            }

        return success, info
