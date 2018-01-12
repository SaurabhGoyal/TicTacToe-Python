import json
import logging

from flask import Flask, request

from game_manager_dialogflow import GameManagerDialogFlow


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)
game_manager_map = {}


@app.route('/')
def home():
    return 'Welcome to TicTacToe world.'


df_game_manager_map = {}


@app.route('/dialogflow-handler', methods=['POST'])
def dialogflow_handler():

    req_data = json.loads(request.data)['result']
    logger.debug(1212, request.data)
    action = req_data['action']
    parameters = req_data['parameters']
    gmdf = None
    expect_user_response = True
    if action == 'start-game':
        user_id = parameters.get('username')
        player_symbol = parameters.get('player-symbol', 'x')
        first_turn = parameters.get('first-turn') == 'yes'
        gmdf = GameManagerDialogFlow()
        df_game_manager_map[user_id] = gmdf
        logger.debug(1313, user_id, player_symbol, first_turn)
        messages = gmdf.start_game(player=player_symbol, first_turn=first_turn)
        logger.debug(1414, messages)

    elif action == 'make-move':
        user_id = req_data.get('contexts')[0]['parameters']['username']
        move = parameters.get('move-location')
        logger.debug(2323, user_id, move)
        if user_id in df_game_manager_map:
            gmdf = df_game_manager_map[user_id]
            messages = gmdf.play_human_move(move=move)
        else:
            messages = ['No active game for user.']
        logger.debug(2424, messages)

    speech = '. '.join([msg['speech'] if isinstance(msg, dict) else msg for msg in messages])
    display_text = '\n'.join([msg['display_text'] if isinstance(msg, dict) else msg for msg in messages])

    logger.debug(3333, speech)
    logger.debug(3434, display_text)

    fulfillment_data = {
        'speech': speech,
        'displayText': display_text,
        'data': {
            'google': {
                'expect_user_response': bool(gmdf and not gmdf.gms.is_over()),
            }
        }
    }

    response = app.response_class(
        response=json.dumps(fulfillment_data),
        status=200,
        mimetype='application/json'
    )
    return response
