import pytest
import json

import connexion

from .context import pylgrum_server

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('../openapi/openapi.yaml')

@pytest.fixture
def client():
    flask_app.app.config['TESTING'] = True

    yield flask_app.app.test_client()

    flask_app.app.test_client().delete('/v1/players')

@pytest.fixture
def client_with_players(client):
    assert(client.post('/v1/players', json={ "name": "jane_hancock" }
    ).status_code == 200)
    assert(client.post('/v1/players', json={ "name": "john_doe" }
    ).status_code == 200)
    assert(client.post('/v1/players', json={ "name": "cayce_pollard" }
    ).status_code == 200)

    yield client

    client.delete('/v1/players')

def registered_players(my_fixture):
    """Returns a list of valid player_ids

    Utility function to keep tests DRY
    """
    r = my_fixture.get('/v1/players')
    rj = json.loads(r.data)['players']
    return [x['id'] for x in rj]

def test_no_players(client):
    """No players registered, we should get an empty list."""
    r = client.get('/v1/players')
    assert(r.status_code == 200)
    assert(len(json.loads(r.data)['players']) == 0)

def test_new_player(client):
    """Register a player."""
    r = client.post(
        '/v1/players',
        json={ "name": "spartacus" }
    )
    assert(r.status_code == 200)
    rj = json.loads(r.data)
    assert(rj['name'] == "spartacus")

def test_null_new_player_fails(client):
    """Register a player."""
    r = client.post(
        '/v1/players',
        json={ }
    )
    assert(r.status_code == 400)

def test_delete_players(client_with_players):
    # confirm that we have non-zero players now
    assert(len(registered_players(client_with_players)) > 0)

    # delete them
    r = client_with_players.delete('/v1/players')
    assert(r.status_code == 200)

    # verify that it's now zero
    assert(len(registered_players(client_with_players)) == 0)

def test_list_players(client_with_players):
    r = client_with_players.get('/v1/players')
    assert(r.status_code == 200)
    rj = json.loads(r.data)['players']
    assert(len(rj) == 3)

def test_create_game(client_with_players):
    r = client_with_players.get('/v1/players')
    assert(r.status_code == 200)
    rj = json.loads(r.data)['players']

    # acting as the first player in the list, start a game with
    #  the last player in the list
    r = client_with_players.post(
        '/v1/games',
        data=json.dumps({
            "player": {
                "id": rj[0]['id'],
                "name": rj[0]['name']
            },
            "opponent_id": rj[-1]['id']
        }),
        content_type='application/json'
    )

    assert(r.status_code == 200)
    rj = json.loads(r.data)
    assert(isinstance(rj['id'], int))

def test_create_game_with_just_id(client_with_players):
    players = registered_players(client_with_players)

    # acting as the first player in the list, start a game with
    #  the last player in the list
    r = client_with_players.post(
        '/v1/games',
        data=json.dumps({
            "player": {
                "id": players[0],
            },
            "opponent_id": players[-1]
        }),
        content_type='application/json'
    )

    assert(r.status_code == 200)
    rj = json.loads(r.data)
    assert(isinstance(rj['id'], int))

def test_create_game_with_no_player_specified_fails(client_with_players):
    r = client_with_players.post(
        '/v1/games',
        data=json.dumps({
            "player": {
            },
            "opponent_id": 1
        }),
        content_type='application/json'
    )
    assert(r.status_code == 400) # 400 b/c it's coming from connexion's validation

def test_create_game_with_null_player_specified_fails(client_with_players):
    players = registered_players(client_with_players)
    r = client_with_players.post(
        '/v1/games',
        data=json.dumps({
            "opponent_id": players[0]
        }),
        content_type='application/json'
    )
    assert(r.status_code == 400)  # 400 b/c it's coming from connexion's validation

def test_create_game_with_bogus_opponent_specified_fails(client_with_players):
    players = registered_players(client_with_players)
    r = client_with_players.post(
        '/v1/games',
        data=json.dumps({
            "player": {
                "id": players[0]
            },
            "opponent_id": 8573223
        }),
        content_type='application/json'
    )
    assert(r.status_code == 403)

def test_only_one_game_per_player_at_a_time(client_with_players):
    players = registered_players(client_with_players)
    r = client_with_players.post(
        '/v1/games',
        data=json.dumps({
            "player": {
                "id": players[0]
            },
            "opponent_id": players[1]
        }),
        content_type='application/json'
    )
    assert(r.status_code == 200)
    r = client_with_players.post(
        '/v1/games',
        data=json.dumps({
            "player": {
                "id": players[0]
            },
            "opponent_id": players[2]
        }),
        content_type='application/json'
    )
    assert(r.status_code == 403)

# FIXME: add test: initial move on a game

# FIXME: add test: retrieving historical moves on a game