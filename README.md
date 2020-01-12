# PyLGRum - A Python Library for the game Gin Rummy

## Project Notes

* There is fairly comprehensive pydoc.
* Uses PEP-484 style type annotations (mostly).
* Uses pytest, with pytest-randomly

## Overview

... classes, server w/ API

Terminological Note: in general, the PyLGRum classes use Player to refer to one side
of a single specific game, and Contestant to refer to the entity that might play a
number of games.

In the API, however, "Player" is used to refer to what would generally be called
Contestants, because "Player" seems like a much more natural way to describe this, and
encoding an awkward term like Contestants in the API contract seems regrettable. Something
needs to change here - either a new term for Player in the classes or perhaps a refactoring
to eliminate the Player/Contestant difference. Until then, you've been warned.

### TODO

Clarify difference between server-driven operating mode (w/ player hooks) and client-driven
async mode (used w/ API). Consider: can they work together? (I think so.)

## Tests

## API

* for dev, run as `PYTHONPATH=".:${PYTHONPATH}" python pylgrum/pylgrum_server.py`
* is RESTish (definitely not pedantically so)
  * core objects: players, games
    * setup:
      * POST to /players to register
        * POST to /games to start a game
    * game play:
      * POST to /games to start a new game
      * GET game status from /games/{id}/[{move_id}]
      * POST to /games/{id} to make a move
    * admin:
      * GET /players to list current players
      * DELETE /players
      * DELETE /games
* API test UI at {baseURL}/ui

```text
======================> TODO

at some point:
- implement Errors that just passing now
- replace print statements in game play with non-terminal-assuming messages

maybe improvements:
- more pythonic in deck.py (lists)
- Card's *_val() methods ---> properties instead
- CardStack size(), peek() --> properties

```
