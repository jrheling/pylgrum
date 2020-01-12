# PyLGRum - A Python Library for Gin Rummy

## Overview

PyLGRum aims to be a comprehensive Python language library for the card game [Gin Rummy](https://en.wikipedia.org/wiki/Gin_rummy).

It currently includes:

* Classes that model the cards and collections of cards needed to play the game.
* Classes that model a game and the players in that game, supporting two operating modes:
  * A *synchronous* mode driven by a Game object that calls hooks in Player objects to advance the game
  * An *asynchronous* mode appropriate for play through an API
* A loosely REST-ish API supporting networked play

## Motivation & Project Goals

Gin Rummy is a fine game and all, but I hope you have better things to do with your time than play a two-person card game against a computer opponent.

So why PyLGRum?

As somebody who both enjoys playing Gin Rummy and making things with software, I wanted a platform in which I could experiment at scale with different strategies for game play. Basically, I want a way to define and test different Gin Rummy playing algorithms. It also serves as a playground project for different programming and system design techniques.

## Technical Notes

### Project Details

* There is fairly comprehensive pydoc.
* Much of PyLGRum uses PEP-484 style type annotations.
* Uses `pytest`, with `pytest-randomly`. (Older modules use `unittest`, but can be discovered/run by `pytest`.)

## Implementation

... classes, server w/ API (this probably gets replaced w/ pydoc/sphinx)

Terminological Note: in general, the PyLGRum classes use Player to refer to one side
of a single specific game, and Contestant to refer to the entity that might play a
number of games.

In the API, however, "Player" is used to refer to what would generally be called
Contestants, because "Player" seems like a much more natural way to describe this, and
encoding an awkward term like Contestants in the API contract seems regrettable. Something
needs to change here - either a new term for Player in the classes or perhaps a refactoring
to eliminate the Player/Contestant difference. Until then, you've been warned.

...
basic game-play concept

Move objects are exchanged btwn Game and Players
Game enforces state

in sync model, player app may derive directly from Player class
in async model, API impl maintains a proxy of Player - user-facing version is the API client's concern

Note: this means the Player class isn't trusted with game state / rules enforcement (even in sync model)

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
