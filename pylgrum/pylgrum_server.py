#from flask import Flask, jsonify, request, abort
import connexion
import json

from pylgrum import Player, Game

NEXT_PLAYER_ID = 1
PLAYERS = {} # hash of id->{game: id, name: str, player: Player}
NEXT_GAME_ID = 1
GAMES = {}   # hash of id->Game

def list_players():
    global PLAYERS

    r = []
    for p in PLAYERS.keys():
        r.append({"id": p, "name": PLAYERS[p]['name']})
    return { 'players': r }

def delete_players():
    global PLAYERS
    PLAYERS = {}
    return None,200

def register_player(body):
    global NEXT_PLAYER_ID
    global PLAYERS

    player_name = body['name']
    new_id = NEXT_PLAYER_ID
    NEXT_PLAYER_ID += 1
    print("giving player id {} to new player {}".format(new_id, player_name))
    if NEXT_PLAYER_ID in PLAYERS.keys():
        err = "INTERNAL ERROR: player id {} already defined".format(new_id)
        print(err)
        return err, 500
    PLAYERS[new_id] = {'name': player_name, 'game': None}
    return {'id': new_id, 'name': player_name}

def create_game(body):
    global NEXT_GAME_ID
    global GAMES

    ## make sure player is legit/defined (else 403)
    player_id = body['player']['id']
    if player_id not in PLAYERS.keys():
        print("registered players: {}".format(PLAYERS.keys()))
        return {
            'player': {
                'id': player_id
            },
            'details': 'player not registered'
        }, 403

    ## look up opponent
    opponent_id = body['opponent_id']
    if opponent_id not in PLAYERS.keys():
        return {
            'player': {
                'id': opponent_id
            },
            'details': 'requested opponent not registered'
        }, 403

    ## are both players available?
    busy = None
    if (PLAYERS[opponent_id]['game'] is not None):
        busy = str(opponent_id)
    elif (PLAYERS[player_id]['game'] is not None):
        busy = str(player_id)

    if (busy is not None):
        return {
            'player': {
                'id': busy
            },
            'details': 'player already in a game'
        }, 403

    ## create game
    PLAYERS[player_id]['player'] = Player()
    PLAYERS[opponent_id]['player'] = Player()
    game = Game(PLAYERS[player_id]['player'], PLAYERS[opponent_id]['player'])
    description = "game between {}({}) and {}({})".format(
        PLAYERS[player_id]['name'],
        player_id,
        PLAYERS[opponent_id]['name'],
        opponent_id
    )
    print("Starting {}".format(description))
    new_game = NEXT_GAME_ID
    NEXT_GAME_ID += 1
    GAMES[new_game] = game
    PLAYERS[player_id]['game'] = new_game
    PLAYERS[opponent_id]['game'] = new_game

    return {
        'description': description,
        'id': new_game
    }, 200

# @app.route('/games/<int:game_id>/move/<int:move_id>', methods=['GET'])
# def recent_moves(game_id, move_id):
#     """Return moves made since move_id.

#     Parameters:
#     * game_id (int)
#     * move_id (int)

#     Returns a list of public_move structures.

#     NOTE (FIXME?): It might make sense to only return public_move structures
#     for the opponents' moves, and to return full move structures for the player's
#     own moves, since this relieves the client of the need to accurately track
#     state. But for now we'll assume the client knows what's up.
#     """
#     pass

# @app.route('/games/<int:game_id>/move', methods=["POST"])
# def make_move(game_id):
#     """Make a move.

#     Expects a private_move structure in the request, and will return an
#     updated private_move.
#     """
#     pass



if __name__ == "__main__":
    # app = connexion.App(__name__, specification_dir='../openapi')
    app = connexion.App(__name__)
    app.add_api('../openapi/openapi.yaml')
    app.run(
        port=8080,
        debug=True
    )