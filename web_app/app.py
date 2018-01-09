import json

from flask import Flask, request

from game_manager_web import GameManagerWeb


app = Flask(__name__)
game_manager_map = {}


@app.route('/')
def home():
    return 'Welcome to TicTacToe world.'


@app.route('/start')
def start_game():
    user_id = request.args.get('user_id', 1123)
    player_symbol = request.args.get('player_symbol', 'x')
    first_turn = request.args.get('first_turn') or False
    gmw = GameManagerWeb()
    game_manager_map[user_id] = gmw
    res_s, res_d = gmw.start_game(player=player_symbol, first_turn=first_turn)
    response = app.response_class(
        response=json.dumps(res_d),
        status=res_s,
        mimetype='application/json'
    )
    return response


@app.route('/make-move')
def make_move():
    user_id = request.args.get('user_id', 1123)
    move = request.args.get('move')
    gmw = game_manager_map.get(user_id)

    if not gmw:
        res_s, res_d = 400, {'messages': ['No active game for this user.']}
    else:
        if not gmw.status == GameManagerWeb.GAME_STATUS_HUMAN_MOVE_REQUIRED:
            res_s, res_d = 400, {'game_status': gmw.status, 'messages': ['Invalid action.']}
        else:
            res_s, res_d = gmw.play_human_move(move=move)

    response = app.response_class(
        response=json.dumps(res_d),
        status=res_s,
        mimetype='application/json'
    )
    return response
