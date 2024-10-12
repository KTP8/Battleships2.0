# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import random

# Define ship types and their sizes
SHIP_SIZES = {
    "Carrier": 5,
    "Battleship": 4,
    "Cruiser": 3,
    "Submarine": 3,
    "Destroyer": 2
}
# Helper function to create an empty 10x10 grid
def create_grid():
    return [[" " for _ in range(10)] for _ in range(10)]