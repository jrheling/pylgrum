from flask import Flask, jsonify, request, abort
import json

from pylgrum import Player

app = Flask(__name__)

#------------- here are the structures we'll use
player_ref = {
    'id': 1,
    'name': "str"
}

card_ref = {
    'suit': 'H', # S, C, H, D
    'card': 'J'  # A, 2..10, J, Q, K
}

public_move_ref = {
    'game_id': 1,
    'move_id': 1,
    'player_id': 1,
    'card_from': 'DISCARD | DECK',
    'discarded': 'card'
}

#------------- end of structures

############# globals (very temp)
next_player_id = 1
players = {} # hash of id->Player
games = []

#############

# FIXME - URL route prefix
@app.route('/players', methods=['GET'])
def list_players():
    """Lists players that are ready for games."""
    global players

    r = []
    for p in players.keys():
        r.append({"id": p, "name": "player {}".format(p)})
    return jsonify(r)

@app.route('/players', methods=['POST'])
def register_player():
    """Tells the server player is ready for games.

    Parameters:
    * name (string describing player)
    Returns:
    * player_id (int)

    # FIXME: we're ignoring the provided name for now, b/c the base Player
    #     class doesn't handle it yet
    # FIXME: add authn here, for retrieving existing players
    """
    global next_player_id
    global players

    if not request.json:
        print("ERROR: invalid payload in call to /players")
        abort(400)

    req_data = json.loads(request.json)

    if not 'name' in req_data:
        print("ERROR: no 'name' in payload of call to /players")
        abort(400)

    player_name = req_data['name']
    new_id = next_player_id
    next_player_id += 1
    print("giving player id {} to new player {}".format(new_id, player_name))
    if next_player_id in players.keys():
        print("INTERNAL ERROR: player id {} already defined".format(new_id))
        abort(500)
    players[new_id] = Player()
    return jsonify({'id': new_id, 'name': player_name})

@app.route('/players/<int:player_id>/challenge', methods=['POST'])
def create_game(player_id):
    """Create a game vs. <player_id>.

    Request Body:
    * "Player" object for self

    Returns game_id
    """
    print("unimplemented")
    abort(404)

@app.route('/games/<int:game_id>/move/<int:move_id>', methods=['GET'])
def recent_moves(game_id, move_id):
    """Return moves made since move_id.

    Parameters:
    * game_id (int)
    * move_id (int)

    Returns a list of public_move structures.

    NOTE (FIXME?): It might make sense to only return public_move structures
    for the opponents' moves, and to return full move structures for the player's
    own moves, since this relieves the client of the need to accurately track
    state. But for now we'll assume the client knows what's up.
    """
    pass

@app.route('/games/<int:game_id>/move', methods=["POST"])
def make_move(game_id):
    """Make a move.

    Expects a private_move structure in the request, and will return an
    updated private_move.
    """
    pass

if __name__ == "__main__":
    app.run(debug=True)
