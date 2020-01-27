#from flask import Flask, jsonify, request, abort
import connexion
import json

from functools import wraps

from pylgrum.card import Card, Rank, Suit
from pylgrum.player import Player
from pylgrum.game import Game
from pylgrum.server.game_manager import GameManager, Contestant


#### FIXME
# - add auth

gm = GameManager()

## Decorators to validate parameters / game state
def player_exists(func):
    """Return 403 if body['player']['id] is not a valid player."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        fail = False
        try:
            if kwargs['body']['player']['id'] not in gm.contestants:
                fail = True
        except KeyError:
            fail = True

        if fail:
            return {
                'details': 'Specified player not found'
            }, 403
        return func(*args, **kwargs)
    return wrapper

def opponent_exists(func):
    """Return 403 if body['opponent_id'] is not a valid player."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        fail = False
        try:
            if kwargs['body']['opponent_id'] not in gm.contestants:
                fail = True
        except KeyError:
            fail = True

        if fail:
            return {
                'details': 'Specified player not found'
            }, 403
        return func(*args, **kwargs)
    return wrapper

def game_exists(func):
    """Return 404 if 'game_id' param is legit."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        fail = False
        try:
            if kwargs['game_id'] not in gm.games:
                fail = True
        except KeyError:
            fail = True

        if fail:
            return {
                'details': 'Specified game not found'
            }, 404
        return func(*args, **kwargs)
    return wrapper

def player_in_game(func):
    """Return 401 if specified player isn't in specified game.

    Assumes valid player/game.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        player_id = kwargs['body']['player']['id']
        game = gm.games[kwargs['game_id']]
        if player_id not in game.contestant_ids:
            return {
                'details': "Player ID {} requesting status on unrelated game {}".format(
                    player_id, kwargs['game_id'])
            }, 401
        return func(*args, **kwargs)
    return wrapper

def is_players_turn(func):
    """Return 403 if it isn't the specified player's turn to make a move.

    Assumes valid player who is part of the specified game.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        player_id = kwargs['body']['player']['id']
        player = gm.contestants[player_id].current_player
        game = gm.games[kwargs['game_id']]
        if player != game.current_player:
            return {
                'details': "It's not that player's turn to move."
            }, 403
        return func(*args, **kwargs)
    return wrapper

## API method handlers
def list_players():
    return { "players": gm.list_contestants() }

def delete_players():
    gm.delete_contestants()
    return None,200

def register_player(body):
    player_name = body['name']
    c = gm.add_contestant(player_name)
    return {
            "id": c.id,
            "name": c.name,
            "currently_playing": c.is_playing
    }

@player_exists
@opponent_exists
def create_game(body):
    player_id = body['player']['id']
    opponent_id = body['opponent_id']
    try:
        new_game = gm.create_game(player_id, opponent_id)
    except (Contestant.ContestantAlreadyPlaying) as e:
        return {
            'details': str(e)
        }, 403

    return new_game

@player_exists
@game_exists
@player_in_game
def game_status(game_id, body):
    game = gm.games[game_id]
    player_id = body['player']['id']
    return game.status_for(
        gm.contestants[player_id].current_player
    )

@player_exists
@game_exists
@player_in_game
@is_players_turn
def turn_start(game_id, body):
    game = gm.games[game_id]
    player_id = body['player']['id']

    game.start_new_move()

    # connexion + our api spec will reject other cardsource values
    if body['cardsource'] == "discard":
        game.current_move.choose_card_from_discard()
    else:
        game.current_move.choose_card_from_draw()

    game.acquire_card()

    return game.status_for(
        gm.contestants[player_id].current_player
    )

@player_exists
@game_exists
@player_in_game
@is_players_turn
def turn_finish(game_id, body):
    game = gm.games[game_id]
    player_id = body['player']['id']
    discard = body['discard']

    game.current_move.discard(
        Card(
            rank = Rank[discard['card']],
            suit = Suit[discard['suit']]
        )
    )
    game.finalize_move()

    game.next_turn()

    return game.status_for(
        gm.contestants[player_id].current_player
    )


if __name__ == "__main__":
    # app = connexion.App(__name__, specification_dir='../openapi')
    app = connexion.App(__name__)
    app.add_api('../openapi/openapi.yaml')
    app.run(
        port=8080,
        debug=True
    )
