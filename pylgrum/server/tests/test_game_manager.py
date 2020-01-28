import pytest
import json
import uuid

from pylgrum.server.game_manager import GameManager, Contestant
from pylgrum.server.errors import ContestantAlreadyPlaying, InvalidContestant

@pytest.fixture
def gm_with_contestants():

    class GenericContainer():
        pass

    td = GenericContainer()

    td.gm = GameManager()
    td.p1 = td.gm.add_contestant()
    td.p2 = td.gm.add_contestant('p2')

    yield td

@pytest.fixture
def game_underway(gm_with_contestants):
    r = gm_with_contestants.gm.create_game(
        gm_with_contestants.p1.id,
        gm_with_contestants.p2.id
    )
    gm_with_contestants.game_id = r['id']
    yield gm_with_contestants

def test_gm_creation(gm_with_contestants):
    assert(isinstance(gm_with_contestants.gm, GameManager))

def test_unnamed_contestant(gm_with_contestants):
    assert(gm_with_contestants.p1.name == Contestant._DEFAULT_NAME)

def test_named_contestant(gm_with_contestants):
    assert(gm_with_contestants.p2.name == 'p2')

def test_add_contestant():
    gm = GameManager()
    assert(len(gm.list_contestants()) == 0)
    gm.add_contestant()
    assert(len(gm.list_contestants()) == 1)

def test_contestant_starts_out_not_playing(gm_with_contestants):
    assert(gm_with_contestants.p1.is_playing == False)

def test_delete_contestants(gm_with_contestants):
    assert(len(gm_with_contestants.gm.list_contestants()) == 2)
    gm_with_contestants.gm.delete_contestants()
    assert(len(gm_with_contestants.gm.list_contestants()) == 0)

def test_create_game(gm_with_contestants):
    f = gm_with_contestants # typographical shortcut for the fixture
    r = f.gm.create_game(f.p1.id, f.p2.id)
    game_id = r['id']
    print("game_id == {}".format(game_id))
    assert(game_id in f.gm.games)

def test_contestants_added_to_new_game(game_underway):
    f = game_underway # typographical shortcut for the fixture
    assert(f.p1.current_player.game == f.gm.games[f.game_id])
    assert(f.p2.current_player.game == f.gm.games[f.game_id])

def test_bogus_contestant_raises(gm_with_contestants):
    f = gm_with_contestants # typographical shortcut for the fixture
    bogus_contestant = str(uuid.uuid4())
    with pytest.raises(InvalidContestant):
        f.gm.create_game(f.p1.id, bogus_contestant)

def test_contestant_only_plays_one_at_a_time(game_underway):
    f = game_underway # typographical shortcut for the fixture
    new_contestant = f.gm.add_contestant('new contestant')
    with pytest.raises(ContestantAlreadyPlaying):
        f.gm.create_game(f.p1.id, new_contestant.id)

def test_currently_playing_flag_set(game_underway):
    f = game_underway # typographical shortcut for the fixture
    assert(f.p1.is_playing)
    assert(f.p2.is_playing)