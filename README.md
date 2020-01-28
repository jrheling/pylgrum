# PyLGRum - A Python Library for Gin Rummy

## Overview

PyLGRum aims to be a comprehensive Python language library for the card game [Gin Rummy](https://en.wikipedia.org/wiki/Gin_rummy).

It currently includes:

* Classes that model the cards and collections of cards needed to play the game.
* Classes that model a game and the players in that game, supporting two operating modes:
  * A *synchronous* mode driven by a Game object that calls hooks in Player objects to advance the game
  * An *asynchronous* mode appropriate for play through an API

## Motivation & Project Goals

Gin Rummy is a fine game and all, but I hope you have better things to do with your time than play a two-person card game against a computer opponent.

So why PyLGRum?

As somebody who both enjoys playing Gin Rummy and making things with software, I wanted a platform in which I could experiment at scale with different strategies for game play. Basically, I want a way to define and test different Gin Rummy playing algorithms. It also serves as a playground project for different programming and system design techniques.

## Current Status

PyLGRum is substantially complete and working, with the following open issues:

* The challenging player always starts the game
* Game doesn't recognize end of game state yet
* Test coverage on TUI game/player is incomplete

## Technical Documentation

The PyLGRum package is [thoroughly documented here](https://jrheling.github.io/pylgrum/pylgrum/).

## TODOs
```text
at some point:
- replace print statements in game play with non-terminal-assuming messages

maybe improvements:
- more pythonic in deck.py (lists)
- Card's *_val() methods ---> properties instead
- CardStack size(), peek() --> properties

```
