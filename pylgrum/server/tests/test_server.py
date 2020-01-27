import pytest
import json
import uuid

import connexion

from pylgrum.server import server

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('../../../openapi/openapi.yaml')

def is_UUID(s: str) -> bool:
    """True if parameter looks like a valid UUID."""
    try:
        uuid.UUID(s)
    except ValueError:
        return False

    return True

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

@pytest.fixture
def client_with_game(client_with_players):
    players = registered_player_ids(client_with_players)
    testdata = {}

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
    testdata['player1_id'] = players[0]
    testdata['player2_id'] = players[-1]
    testdata['game_id'] = json.loads(r.data)['id']
    testdata['players'] = players
    client_with_players.testdata = testdata

    yield client_with_players

    client_with_players.delete('/v1/players')


def registered_player_ids(my_fixture):
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
    assert(len(registered_player_ids(client_with_players)) > 0)

    # delete them
    r = client_with_players.delete('/v1/players')
    assert(r.status_code == 200)

    # verify that it's now zero
    assert(len(registered_player_ids(client_with_players)) == 0)

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
    assert(is_UUID(rj['id']))

def test_create_game_with_just_id(client_with_players):
    players = registered_player_ids(client_with_players)

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
    assert(is_UUID(rj['id']))

def test_create_game_with_no_player_specified_fails(client_with_players):
    players = registered_player_ids(client_with_players)

    r = client_with_players.post(
        '/v1/games',
        data=json.dumps({
            "player": {
            },
            "opponent_id": players[0]
        }),
        content_type='application/json'
    )
    print(r.status_code)
    assert(r.status_code == 403)

def test_create_game_with_null_player_specified_fails(client_with_players):
    players = registered_player_ids(client_with_players)
    r = client_with_players.post(
        '/v1/games',
        data=json.dumps({
            "opponent_id": players[0]
        }),
        content_type='application/json'
    )
    print(r.status_code)
    assert(r.status_code == 400)

def test_create_game_with_bogus_opponent_specified_fails(client_with_players):
    players = registered_player_ids(client_with_players)
    r = client_with_players.post(
        '/v1/games',
        data=json.dumps({
            "player": {
                "id": players[0]
            },
            "opponent_id": str(uuid.uuid4())
        }),
        content_type='application/json'
    )
    assert(r.status_code == 403)

def test_only_one_game_per_player_at_a_time(client_with_players):
    players = registered_player_ids(client_with_players)
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

def test_game_status_returns(client_with_game):
    r = client_with_game.post(
        '/v1/games/{}'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
        }),
        content_type='application/json'
    )

    assert(r.status_code == 200)
    rj = json.loads(r.data)
    assert(isinstance(rj['current_player'], str))

def test_game_status_returns_hand_to_player1(client_with_game):
    r = client_with_game.post(
        '/v1/games/{}'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
        }),
        content_type='application/json'
    )

    assert(r.status_code == 200)
    rj = json.loads(r.data)
    assert(len(rj['hand']) == 10)

def test_game_status_returns_hand_to_player2(client_with_game):
    r = client_with_game.post(
        '/v1/games/{}'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player2_id'],
            },
        }),
        content_type='application/json'
    )

    assert(r.status_code == 200)
    rj = json.loads(r.data)
    assert(len(rj['hand']) == 10)

def test_game_status_request_from_non_player_fails(client_with_game):
    td = client_with_game.testdata

    # find a player who is legit but isn't in this game
    for p in td['players']:
        if p == td['player1_id']:
            continue
        if p == td['player2_id']:
            continue
        non_player = p
        break

    r = client_with_game.post(
        '/v1/games/{}'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": non_player,
            },
        }),
        content_type='application/json'
    )

    assert(r.status_code == 401)

def test_game_status_request_from_bogus_player_fails(client_with_game):
    bogus_player = str(uuid.uuid4())

    r = client_with_game.post(
        '/v1/games/{}'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": bogus_player,
            },
        }),
        content_type='application/json'
    )

    assert(r.status_code == 403)

def test_game_status_request_with_no_player_fails(client_with_game):
    r = client_with_game.post(
        '/v1/games/{}'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
            },
        }),
        content_type='application/json'
    )

    assert(r.status_code == 403)

def test_game_status_for_invalid_gameid_fails(client_with_game):
    bogus_gameid = str(uuid.uuid4())

    r = client_with_game.post(
        '/v1/games/{}'.format(bogus_gameid),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
        }),
        content_type='application/json'
    )

    assert(r.status_code == 404)

def test_illegal_card_source_fails(client_with_game):
    r = client_with_game.post(
        '/v1/games/{}/move'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
            "cardsource": "schmorpful"
        }),
        content_type='application/json'
    )

    assert(r.status_code == 400) # is a 400 b/c connexion validation should catch it

def test_choose_discard(client_with_game):
    discard = json.loads(client_with_game.post(
        '/v1/games/{}'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
        }),
        content_type='application/json'
    ).data)['visible_discard']

    r = client_with_game.post(
        '/v1/games/{}/move'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
            "cardsource": "discard"
        }),
        content_type='application/json'
    )

    assert(r.status_code == 200)
    assert(json.loads(r.data)['new_card'] == discard)

def test_choose_draw(client_with_game):
    r = client_with_game.post(
        '/v1/games/{}/move'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
            "cardsource": "deck"
        }),
        content_type='application/json'
    )

    assert(r.status_code == 200)
    # that the correct card is acquired here is tested at a lower level - here
    #   we're ok just knowing a card came back.
    assert(isinstance(json.loads(r.data)['new_card']['suit'], str))
    assert(isinstance(json.loads(r.data)['new_card']['card'], str))

def test_start_move_when_not_your_turn_fails(client_with_game):
    r = client_with_game.post(
        '/v1/games/{}/move'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player2_id'],
            },
            "cardsource": "discard"
        }),
        content_type='application/json'
    )
    assert(r.status_code == 403)

def test_status_after_acquisition_works(client_with_game):
    discard = json.loads(client_with_game.post(
        '/v1/games/{}'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
        }),
        content_type='application/json'
    ).data)['visible_discard']

    r = client_with_game.post(
        '/v1/games/{}/move'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
            "cardsource": "discard"
        }),
        content_type='application/json'
    )

    assert(r.status_code == 200)
    assert(json.loads(r.data)['new_card'] == discard)

    new_game_status = client_with_game.post(
        '/v1/games/{}'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
        }),
        content_type='application/json'
    )
    assert(new_game_status.status_code == 200)

def test_do_discard(client_with_game):
    # take card from discard pile, then discard first card from hand
    starting_status = json.loads(client_with_game.post(
        '/v1/games/{}'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
        }),
        content_type='application/json'
    ).data)

    acquired_card = starting_status['visible_discard']
    discarded_card = starting_status['hand'][0]

    ## take from the discard pile
    r = client_with_game.post(
        '/v1/games/{}/move'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
            "cardsource": "discard"
        }),
        content_type='application/json'
    )

    assert(r.status_code == 200)
    assert(json.loads(r.data)['new_card'] == acquired_card)

    ## disard the first card in hand
    r = client_with_game.patch(
        '/v1/games/{}/move'.format(client_with_game.testdata['game_id']),
        data=json.dumps({
            "player": {
                "id": client_with_game.testdata['player1_id'],
            },
            "discard": discarded_card
        }),
        content_type='application/json'
    )

    assert(r.status_code == 200)
    rj = json.loads(r.data)
    # play should have shifted to the other player
    assert(rj['current_player'] != client_with_game.testdata['player1_id'])
    # the currently showing discard should be the card we just discarded
    assert(rj['visible_discard'] == discarded_card)


# FIXME: add test: initial move on a game

# FIXME: add test: retrieving historical moves on a game