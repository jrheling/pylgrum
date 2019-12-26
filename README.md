# PyLGRUM - A Python Library for the game Gin Rummy

## Project Notes

* There is fairly comprehensive pydoc.
* Uses PEP-484 style type annotations (mostly).
* Uses pytest, with pytest-randomly

## Tests

## API

* tries to be RESTful
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
