"""
test_battleships.py

This file performs comprehensive checking of critical functions in the Battleships game
using Python's unittest framework.

Functions Tested:
    - create_grid: Ensures the grid is created with the correct dimensions.
    - validate_guess: Checks that empty input, out-of-bound coordinates, valid input, 
      and duplicate guesses are handled correctly.
    - check_if_ship_sunk: Simulates hitting parts of a ship and verifies if the ship is 
      considered sunk.

Instructions to Run the Tests:
1. Place this file in the root directory alongside run.py.
2. Open a terminal in the root directory.
3. Run the tests with the command:
       python -m unittest discover
   or simply run:
       python test_battleships.py
4. The test output will show which tests passed or if any failed.
"""

import unittest
from run import Battleships, create_grid

class TestBattleships(unittest.TestCase):
    def setUp(self):
        # Create a new game instance and an empty grid before each test
        self.game = Battleships()
        self.grid = create_grid()

    def test_create_grid_dimensions(self):
        # Verify that create_grid returns a 10x10 grid
        grid = create_grid()
        self.assertEqual(len(grid), 10, "Grid should have 10 rows")
        for row in grid:
            self.assertEqual(len(row), 10, "Each row should have 10 columns")

    def test_validate_guess_empty(self):
        # Check that an empty guess returns False
        result = self.game.validate_guess("", self.grid)
        self.assertFalse(result, "Empty input should return False")

    def test_validate_guess_valid(self):
        # Check that a valid guess returns a tuple (row, col)
        result = self.game.validate_guess("3,4", self.grid)
        self.assertEqual(result, (3, 4), "A valid guess should return (3, 4)")

    def test_validate_guess_out_of_bounds(self):
        # Check that a guess with coordinates outside the grid returns False
        result = self.game.validate_guess("10,10", self.grid)
        self.assertFalse(result, "Out-of-bound coordinates should return False")

    def test_validate_guess_duplicate(self):
        # Simulate a duplicate guess by marking cell (2,3) as already guessed
        self.grid[2][3] = "X"
        result = self.game.validate_guess("2,3", self.grid)
        self.assertEqual(result, "duplicate", "A duplicate guess should return 'duplicate'")

    def test_check_if_ship_sunk(self):
        # Create a ship with coordinates (2,2), (2,3), (2,4) and simulate hits
        ship = [(2, 2), (2, 3), (2, 4)]
        self.game.player_ships = [ship.copy()]
        # Hit (2,2) - ship should not be sunk yet
        sunk = self.game.check_if_ship_sunk(self.game.player_ships, 2, 2)
        self.assertFalse(sunk, "Ship should not be sunk after one hit")
        # Hit (2,3) - ship should still not be sunk
        sunk = self.game.check_if_ship_sunk(self.game.player_ships, 2, 3)
        self.assertFalse(sunk, "Ship should not be sunk after two hits")
        # Hit (2,4) - ship should now be sunk
        sunk = self.game.check_if_ship_sunk(self.game.player_ships, 2, 4)
        self.assertTrue(sunk, "Ship should be sunk after all parts are hit")

if __name__ == '__main__':
    unittest.main()
