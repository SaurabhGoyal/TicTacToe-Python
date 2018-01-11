import json

from flask import Flask, request

from game_manager_dialogflow import GameManagerDialogFlow


app = Flask(__name__)
game_manager_map = {}


@app.route('/')
def home():
    return 'Welcome to TicTacToe world.'


df_game_manager_map = {}


@app.route('/dialogflow-handler', methods=['POST'])
def dialogflow_handler():

    req_data = json.loads(request.data)['result']
    # print(1212, request.data)
    action = req_data['action']
    parameters = req_data['parameters']
    if action == 'start-game':
        user_id = parameters.get('username')
        player_symbol = parameters.get('player-symbol', 'x')
        first_turn = parameters.get('first-turn') == 'yes'
        gmdf = GameManagerDialogFlow()
        df_game_manager_map[user_id] = gmdf
        print(1313, user_id, player_symbol, first_turn)
        messages = gmdf.start_game(player=player_symbol, first_turn=first_turn)
        print(1414, messages)

    elif action == 'make-move':
        user_id = req_data.get('contexts')[0]['parameters']['username']
        move = parameters.get('move-location')
        print(2323, user_id, move)
        if user_id in df_game_manager_map:
            gmdf = df_game_manager_map[user_id]
            messages = gmdf.play_human_move(move=move)
        else:
            messages = ['No active game for user.']
        print(2424, messages)

    # msg = messages[0]

    response = app.response_class(
        response=json.dumps({'speech': '', 'messages': [{'type': 0, 'speech': msg} for msg in messages]}),
        status=200,
        mimetype='application/json'
    )
    return response
