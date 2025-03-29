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
                
                # Validate orientation input
                while True:
                    orientation = input("Choose orientation (H for horizontal, V for vertical): ").upper().strip()
                    if orientation in ["H", "V"]:
                        break
                    else:
                        print("Invalid orientation. Please enter 'H' or 'V'.")
                
                print("\nCoordinate system is as follows: top left corner of the board is (0,0) \nand bottom right corner is (9,9)")
                print("\nHorizontal ships fill the spaces from left (start coordinate) to right & \nVertical ships fill the spaces from top (start coordinate) down.")
                print("\nEnter starting coordinates as (row,col) between (0,0) and (9,9).")
                
                # Validate coordinate input
                while True:
                    coord_input = input(f"Enter starting coordinates for your {ship_name} \n(row,col) WITHOUT parenthesis '()': ").strip()
                    try:
                        row, col = map(int, coord_input.split(","))
                        if row < 0 or row > 9 or col < 0 or col > 9:
                            print("Coordinates out of bounds. Please enter numbers between 0 and 9.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter two numbers separated by a comma (e.g., 3,5).")
                    except Exception as e:
                        print(f"Unexpected error: {e}. Please try again.")
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

    # Place all ships for a player
    def place_all_ships(self):
        print("Place your ships on the board.")
        for ship, size in SHIP_SIZES.items():
            self.place_ship(self.player_board, size, ship)
        print("\nComputer is placing its ships.")
        for ship, size in SHIP_SIZES.items():
            self.place_ship(self.computer_board, size, ship)

    # Review ship placement and give player option to modify
    def review_ship_placement(self):
        while True:
            print("\nYour final ship placement:")
            display_grid(self.player_board)
            happy = ""
            while happy not in ["yes", "no"]:
                happy = input("Are you happy with your ship placement? (yes/no): ").lower().strip()
                if happy not in ["yes", "no"]:
                    print("Please answer 'yes' or 'no'.")
            if happy == "yes":
                break
            else:
                print("\nCurrent ship placements:")
                for i, ship in enumerate(SHIP_SIZES.keys()):
                    print(f"{i+1}. {ship}: {self.player_ships[i]}")
                ship_to_move = input("Enter the name of the ship you want to move: ").capitalize()
                if ship_to_move in SHIP_SIZES:
                    self.move_ship(ship_to_move)
                else:
                    print("Invalid ship name. Please try again.")

    # Move a ship to new coordinates
    def move_ship(self, ship_name):
        index = list(SHIP_SIZES.keys()).index(ship_name)
        old_coordinates = self.player_ships[index]
        for r, c in old_coordinates:
            self.player_board[r][c] = " "  # Clear old ship position

        size = SHIP_SIZES[ship_name]
        print(f"\nEnter new placement for {ship_name} (size {size}):")
        self.place_ship(self.player_board, size, ship_name)

    # Validate a guess to ensure it is within bounds and has not been guessed already
    def validate_guess(self, guess, guesses_board):
        # Check for empty input first
        if not guess.strip():
            print("Empty guess is not allowed. Please enter a valid guess (e.g., 2,3).")
            return False
        try:
            row, col = map(int, guess.split(","))
            if (row < 0 or row >= 10) or (col < 0 or col >= 10):
                print("Coordinates out of bounds. \nPlease enter coordinates between (0,0) and (9,9) WITHOUT parenthesis '()'.")
                return False
            if guesses_board[row][col] != " ":
                print("You have already guessed those coordinates. Try again.")
                return False
            return (row, col)
        except ValueError:
            print("Invalid input. Please enter row,col (e.g., 2,3).")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}. Please enter a valid guess.")
            return False

    # Handle player's turn
    def player_turn(self):
        while True:
            guess = input("Enter your guess (row,col) \nbetween (0,0) and (9,9) WITHOUT parenthesis '()': ")
            validated_guess = self.validate_guess(guess, self.player_guesses_board)
            if validated_guess:
                row, col = validated_guess
                self.player_guesses.append((row, col))
                if self.computer_board[row][col] == "O":
                    print("Hit!")
                    self.player_guesses_board[row][col] = "*"
                    self.computer_board[row][col] = "*"
                    if self.check_if_ship_sunk(self.computer_ships, row, col):
                        self.player_sunk_ships += 1
                        print("Congratulations! You sank a computer's ship.")
                else:
                    print("Miss!")
                    self.player_guesses_board[row][col] = "X"
                break
    
    # Check if the entire ship is sunk
    def check_if_ship_sunk(self, ships, row, col):
        for ship in ships:
            if (row, col) in ship:
                ship.remove((row, col))
                if not ship:  # Ship has been completely sunk
                    return True
        return False

    # Handle computer's turn for both easy and hard levels
    def computer_turn(self, difficulty="easy"):
        if difficulty == "easy":
            self.random_computer_turn()
        elif difficulty == "hard":
            self.smart_computer_turn()
    
    def random_computer_turn(self):
        while True:
            row, col = random.randint(0, 9), random.randint(0, 9)
            if (row, col) not in self.computer_guesses:
                self.computer_guesses.append((row, col))
                print(f"Computer guessed: {row},{col}")
                if self.player_board[row][col] == "O":
                    print("Computer hit one of your ships!")
                    self.computer_guesses_board[row][col] = "*"
                    self.player_board[row][col] = "*"
                    self.last_computer_hit = (row, col)
                    if self.check_if_ship_sunk(self.player_ships, row, col):
                        self.computer_sunk_ships += 1
                        print(f"The computer has sunk one of your ships!")
                        self.last_computer_hit = None
                else:
                    print("Computer missed!")
                    self.computer_guesses_board[row][col] = "X"
                    self.last_computer_hit = None
                break

    # Smart logic for hard difficulty
    def smart_computer_turn(self):
        if self.last_computer_hit and self.last_hit_direction:
            row, col = self.last_computer_hit
            if self.last_hit_direction == "H":
                possible_guesses = [(row, col + 1), (row, col - 1)]
            else:
                possible_guesses = [(row + 1, col), (row - 1, col)]
        elif self.last_computer_hit:
            row, col = self.last_computer_hit
            possible_guesses = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
            random.shuffle(possible_guesses)
        else:
            self.random_computer_turn()
            return

        for r, c in possible_guesses:
            if (r, c) not in self.computer_guesses and 0 <= r < 10 and 0 <= c < 10:
                self.computer_guesses.append((r, c))
                print(f"Computer guessed: {r},{c}")
                if self.player_board[r][c] == "O":
                    print("Computer hit one of your ships!")
                    self.computer_guesses_board[r][c] = "*"
                    self.player_board[r][c] = "*"
                    self.last_computer_hit = (r, c)
                    if self.check_if_ship_sunk(self.player_ships, r, c):
                        self.computer_sunk_ships += 1
                        print(f"The computer has sunk one of your ships!")
                        self.last_computer_hit = None
                        self.last_hit_direction = None
                    else:
                        if self.last_hit_direction is None:
                            if r == row:
                                self.last_hit_direction = "H"
                            else:
                                self.last_hit_direction = "V"
                else:
                    print("Computer missed!")
                    self.computer_guesses_board[r][c] = "X"
                    if self.last_hit_direction:
                        self.last_hit_direction = None
                    break

    # Check if all ships have been sunk
    def all_ships_sunk(self, board):
        for row in board:
            if "O" in row:
                return False
        return True

    # Main game loop with alternating turns
    def play_game(self, difficulty="easy"):
        print("Welcome to Battleships!")
        print("\nInstructions:")
        print("- 'O' represents placement of your ships.")
        print("- 'X' represents a missed hit.")
        print("- '*' represents a successful hit.")
        print("You will place your ships and then take turns guessing where the \ncomputer's ships are located.")
        print("The computer will also guess where your ships are hidden.")
        print("The game ends when one player sinks all of the other's ships!\n")
        
        # Validate player's name with exception handling
        while True:
            try:
                player_name = input("Enter your name: ").strip()
            except Exception as e:
                print(f"Unexpected error reading your name: {e}. Please try again.")
                continue
            if not player_name:
                print("Name cannot be blank. Please enter your name.")
                continue
            break
        print(f"Hello, {player_name}. Let's start!")

        self.place_all_ships()
        self.review_ship_placement()

        while True:
            # Display scoreboard
            print(f"\nScoreboard: {player_name} {self.player_sunk_ships} - {self.computer_sunk_ships} Computer")
            
            # Player's turn
            print("\nYour Guess Board:")
            display_grid(self.player_guesses_board)
            print("\nComputer's Guess Board (with your ships visible):")
            display_grid(self.computer_guesses_board, hide_ships=True, player_board=self.player_board)  # Ensure ships are visible
            self.player_turn()

            if self.all_ships_sunk(self.computer_board):
                print(f"\nThe score is {player_name} 5 - {self.computer_sunk_ships} Computer.")
                print(f"Congratulations, {player_name}! You sank all the computer's ships. You win!")
                break

            # Computer's turn
            print("\nComputer's turn:")
            self.computer_turn(difficulty=difficulty)

            if self.all_ships_sunk(self.player_board):
                print(f"\nThe score is {player_name} {self.player_sunk_ships} - 5 Computer.")
                print("All your ships have been sunk. The computer wins.")
                break

# Start the game
if __name__ == "__main__":
    # Validate difficulty input
    while True:
        difficulty = input("Choose difficulty (easy/hard): ").strip().lower()
        if difficulty in ["easy", "hard"]:
            break
        else:
            print("Invalid difficulty. Please type 'easy' or 'hard'.")
    game = Battleships()
    game.play_game(difficulty=difficulty)
