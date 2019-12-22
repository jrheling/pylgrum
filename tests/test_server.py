import pytest
import json

from .context import pylgrum_server

@pytest.fixture(scope="session")
def client():
    pylgrum_server.app.config['TESTING'] = True
    return pylgrum_server.app.test_client()

@pytest.fixture(scope="session")
def client_with_players(client):
    assert(client.post('/players', json=json.dumps(
        { "name": "jane_hancock" }
    )).status_code == 200)
    assert(client.post('/players', json=json.dumps(
        { "name": "john_doe" }
    )).status_code == 200)
    return client

def test_no_players(client):
    """No players registered, we should get an empty list."""
    r = client.get('/players')
    assert(r.status_code == 200)
    assert(len(json.loads(r.data)) == 0)

def test_new_player(client):
    """Register a player."""
    r = client.post('/players', json=json.dumps(
        { "name": "spartacus" }
    ))
    assert(r.status_code == 200)
    rj = json.loads(r.data)
    assert(rj['name'] == "spartacus")

# FIXME: add test: player POST w/ no payload is error

def test_list_players(client_with_players):
    r = client_with_players.get('/players')
    assert(r.status_code == 200)
    rj = json.loads(r.data)
    #FIXME won't work until base Player class uses names
    #assert(any(x['name'] == 'john_doe' for x in rj))
    assert(len(rj) == 3)

def test_create_game(client_with_players):
    r = client_with_players.get('/players')
    assert(r.status_code == 200)
    rj = json.loads(r.data)

    # acting as the first player in the list, start a game with
    #  the last player in the list
    url = "/players/{}/challenge".format(rj[-1]['id'])
    r = client_with_players.post(url, json=rj[0])
    assert(r.status_code == 200) ##### EXPECTED TO FAIL AT THE MOMENT
    game_id = json.loads(r.data)
    assert(isinstance(game_id, int))

# FIXME: add test: initial move on a game

# FIXME: add test: retrieving historical moves on a game
