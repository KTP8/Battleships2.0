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

# Class for the Battleships game
class Battleships:
    def __init__(self):
        self.player_board = create_grid()
        self.computer_board = create_grid()
        self.player_guesses_board = create_grid()
        self.computer_guesses_board = create_grid()
        self.player_guesses = []
        self.computer_guesses = []
        self.player_sunk_ships = 0
        self.computer_sunk_ships = 0
        self.last_computer_hit = None
        self.last_hit_direction = None
        self.possible_next_guesses = []
        self.player_ships = []
        self.computer_ships = []

    # Display board after placing a ship to show its position
    def display_board_with_ships(self):
        print("\nCurrent board with placed ships:")
        display_grid(self.player_board)

    # Place a ship on a grid with real-time display of ship placement
    def place_ship(self, board, ship_size, ship_name):
        while True:
            if board == self.player_board:
                self.display_board_with_ships()  # Show current state of the board with ships
                print(f"\nPlace your {ship_name} (size {ship_size}).")
                orientation = input("Choose orientation (H for horizontal, V for vertical): ").upper() 
                print("\nCoordinate system is as follows: top left corner of the board is (0,0) and bottom right corner is (9,9)")
                print("\nHorizontal ships fill the spaces from left (start coordinate) to right & Vertical ships fill the spaces from top (start coordinate) down.")
                print("\nEnter starting coordinates as (row,col) between (0,0) and (9,9).")
                row, col = map(int, input(f"Enter starting coordinates for your {ship_name} (row,col) without parenthesis: ").split(","))
            else:
                orientation = random.choice(["H", "V"])
                row, col = random.randint(0, 9), random.randint(0, 9)

            ship_coordinates = []

            if orientation == "H":
                if col + ship_size <= 10 and all(board[row][c] == " " for c in range(col, col + ship_size)):
                    for c in range(col, col + ship_size):
                        board[row][c] = "O"  # Use "O" to represent ships
                        ship_coordinates.append((row, c))
                    break
            elif orientation == "V":
                if row + ship_size <= 10 and all(board[r][col] == " " for r in range(row, row + ship_size)):
                    for r in range(row, row + ship_size):
                        board[r][col] = "O"  # Use "O" to represent ships
                        ship_coordinates.append((r, col))
                    break

            if board == self.player_board:
                print("Invalid placement. Try again.")
                
        # Add ship coordinates to the respective player/computer's ship list
        if board == self.player_board:
            self.player_ships.append(ship_coordinates)
        else:
            self.computer_ships.append(ship_coordinates)