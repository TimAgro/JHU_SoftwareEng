import unittest
import numpy as np

import game
import util

from constants import (
    WeaponType,
    SuspectType,
    RoomType,
    HallwayType,
    MoveOps,
    MoveRes,
    N_GRID,
    CORNERS,
)
from util import (
    suspect_init_hallway,
    grid2pos,
    pos2grid,
    print_line,
)

class Test(unittest.TestCase):
    
    ###Do unit tests
    def test_create_gameboard(self):
        print("#########################Create game board2#########################")
        gb = game.GameBoard(3)
        print(np.array(gb.player_grid))
        print(np.array(gb.room_grid))

    def test_create_grid(self):
        print("#########################Grid#########################")
        print(util.grid2pos(6))
        print(util.grid2pos(4))
        print(util.grid2pos(10))

    def test_gamemanager(self):
        print("#########################Create game manager#########################")
        gm = game.GameManager([1,2,3,4,5,6],1)
        print(gm.players)

    def test_check_turn(self):
        print("#########################Check turn#########################")
        gm = game.GameManager([1,2,3,4,5,6],1)
        print(gm.check_turn(1))

    def test_move(self):
        print("#########################move player#########################")
        gm = game.GameManager([1,2,3,4,5,6],1)
        print(np.array(gm.gb.player_grid))
        print(gm.move(1,"down"))
        print(gm.move(2,"down"))
        print(gm.move(2,"left"))
        print(gm.move(3,"up"))
        print(gm.move(3,"right"))
        print(gm.move(4,"left"))
        print(gm.move(4,"up"))
        print(gm.move(5,"left"))
        print(gm.move(5,"up"))
        print(gm.move(6,"left"))
        print(gm.move(6,"up"))
        print(gm.move(1,"secret"))
        print(np.array(gm.gb.player_grid))

    def test_secret_move(self):
        print("#########################move player#########################")
        gm = game.GameManager([1,2,3,4,5,6],1)
        print(np.array(gm.gb.player_grid))
        print(gm.move(1,"up"))
        print(np.array(gm.gb.player_grid))

    def test_deck(self):
        print("########################DECK##################")
        deck = game.Deck(3)
        print(deck.deck)
        print(deck.solution)
        print(deck.hands)

    def test_accusation(self):
        print("#########################Accusation#########################")
        gm = game.GameManager([1,2,3,4,5,6],1)
        solution  = gm.deck.solution
        result = gm.check_accusation(1, solution[0], solution[1], solution[2])
        print(result)

    def test_suggestion(self):
        print("#########################Suggestion#########################")
        gm = game.GameManager([1,2,3,4,5,6],1)
        solution  = gm.deck.solution
        print(np.array(gm.deck.hands))
        result = gm.check_suggestion(1, 'KNIFE', 'PROF_PLUM', 'LOUNGE')
        print(result)
        result = gm.check_suggestion(1, solution[0], solution[1], solution[2])
        print(result)

    def test_get_player_room(self):
        print("#########################GET PLAYER ROOM#########################")
        gm = game.GameManager([1,2,3,4,5,6],1)
        result = gm.get_player_room(1)
        print(result)

if __name__ == '__main__':
	#When tests.py is called in command line, all unit tests will be run sequentially
	unittest.main()
