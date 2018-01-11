from core import constants as core_constants
from core.game_manager_service import GameManagerService


class GameManagerCLI:
    """ A class to manage a TicTacToe game in CLI """

    def __init__(self, **kwargs):
        self.gms = GameManagerService()

    def start_game(self, **kwargs):
        """ starts a new game """

        success, info = self.gms.start_game(
            player=kwargs.get('player', 'x'),
            first_turn=raw_input('Would you like to go first? y/n\n') == 'y'
        )
        if success:
            if info['status_code'] == core_constants.GAME_STATUS_HUMAN_MOVE_REQUIRED:
                print(self.gms.game.get_board_state_pretty())
                self.play_human_move()
        else:
            print(info['messages'][0])

    def play_human_move(self):
        """ Takes input from user and plays human move and decides further """
        success, info = self.gms.play_human_move(raw_input('Make your next move\n'.format('')))
        if success:
            print(self.gms.game.get_board_state_pretty())
            if info['status_code'] == core_constants.GAME_STATUS_HUMAN_MOVE_REQUIRED:
                self.play_human_move()
            elif info['status_code'] in [
                core_constants.GAME_STATUS_OVER_DRAW,
                core_constants.GAME_STATUS_OVER_HUMAN_WINNER,
                core_constants.GAME_STATUS_OVER_COMP_WINNER,
            ]:
                print(self.gms.status_code_message_map[info['status_code']])
        else:
            if info['error_code'] == core_constants.ERROR_CODE_INVALID_MOVE:
                self.play_human_move()


gmc = GameManagerCLI()
gmc.start_game()
