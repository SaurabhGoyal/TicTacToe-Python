from core.game_manager_service import GameManagerService


class GameManagerDialogFlow:
    """ A class to manage a TicTacToe game for DialogFlow """

    def __init__(self, **kwargs):
        self.gms = GameManagerService()

    def start_game(self, player, first_turn, **kwargs):
        """ starts a new game """

        success, info = self.gms.start_game(player=player, first_turn=first_turn)
        messages = []
        if success:
            if not first_turn:
                messages.append({
                    'speech': 'I marked {}'.format(self.gms.get_last_comp_move_display_text()),
                    'display_text': self.gms.game.get_board_state_pretty()
                })
        else:
            messages.extend(info['messages'])
        messages.append(self.gms.get_game_status_message())
        return messages

    def play_human_move(self, move):
        """ Takes input from user and plays human move and decides further """

        success, info = self.gms.play_human_move(move)
        messages = []
        if success:
            messages.append({
                'speech': 'I marked {}'.format(self.gms.get_last_comp_move_display_text()),
                'display_text': self.gms.game.get_board_state_pretty()
            })
            messages.append(self.gms.get_game_status_message())
            if self.gms.is_over():
                messages.append('We are done here.')
        else:
            messages.extend(info['messages'])
            messages.append(self.gms.get_game_status_message())

        return messages
