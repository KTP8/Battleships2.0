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

# Display a grid with labels for rows and columns
def display_grid(grid, hide_ships=False, player_board=None):
    print("  " + " ".join(str(i) for i in range(10)))
    for idx, row in enumerate(grid):
        row_display = []
        for col_idx, cell in enumerate(row):
            if hide_ships:
                # If player_board is provided, display the player's ships on the computer's board using "O"
                if player_board and player_board[idx][col_idx] == "O":
                    row_display.append("O")
                else:
                    row_display.append(" " if cell == "O" else cell)
            else:
                row_display.append(cell)
        print(f"{idx} " + " ".join(row_display))