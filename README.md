cscs-531-rps-tournament
=======================

CSCS 531 RPS Tournament

This is the setup for the University of Michigan Complex Systems 531 
Rock-Paper-Scissors (RPS) tournament.  This repository is meant to be a simple
(and somewhat sloppy) implementation of a base RPS Player, a Referee who
runs the mechanics of RPS tournaments, and a driver for the overall tournament.

The goal is to build out a few different tournament types and metarules, as
well as the basics of handling a bunch of student submissions for Player
agents. 

# Adding an entrant
To add an entrant, create a player that extends our base Player class.  Then, put the player inside of the entrants folder in the root of this repository.

# Running unit tests
$ PYTHONPATH=src/:tests/ python tests/edu/umich/cscs/rps/tests/agents.py
$ PYTHONPATH=src/:tests/ python tests/edu/umich/cscs/rps/tests/tournament.py