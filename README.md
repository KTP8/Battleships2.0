# Battleships Game

[IMG: Project Screenshot]

## Table of Contents
1. [Introduction](#introduction)
2. [Technologies Used](#technologies-used)
3. [Features](#features)
4. [Code Example](#code-example)
5. [Testing](#testing)
6. [Deployment](#deployment)
7. [Credits](#credits)

---

## Introduction

This project is a command-line-based version of the classic Battleships game. Players can place their ships on a grid and take turns against a computer opponent, trying to guess the locations of each other's ships. The game offers two difficulty levels—easy and hard—where the computer can either make random guesses or use strategic logic to attempt to sink the player's ships.

**Very Important Note:** There are a limited number of commits for this project, and it may appear that the project was completed in a short period. However, this is because the wrong template was initially used, and I had to restart the project with the correct format. Despite the limited commits, the project was developed over ample time, and all code is original and not plagiarized.

### Git History with Original Commits:
[IMG: Git Commit History for Incorrect Template]  
[IMG: Git Commit History for Correct Template]

---

## Technologies Used

- **Python 3.12.2**
- **Heroku** for deployment
- **Gitpod** for development environment

---

## Features

### Core Gameplay

- **Player and Computer Ships**: Both the player and the computer can place five types of ships on their respective 10x10 boards.
- **Strategic Guessing**: The player and computer take turns guessing the location of each other's ships. The game tracks hits and misses and shows these on the guess board.
- **Scoreboard**: A live scoreboard updates the number of ships each player has sunk.

### Difficulty Levels:

- **Easy Mode**: In easy mode, the computer makes purely random guesses. There is no strategic thinking, and this mode is best suited for players who prefer a more relaxed and straightforward game experience (best suited to children).
- **Hard Mode**: In hard mode, the computer applies strategic logic. When it registers a hit, the computer continues guessing in the same direction (either horizontally or vertically) to attempt to sink the entire ship. This adds a more challenging and competitive element to the game, making it suitable for experienced players (best suited to experienced players or adults).

### Ship Placement

- The player is prompted to place each of their ships and can preview their placements after every selection.
- The preview feature allows players to see how their ship layout is coming together, avoiding overlaps and giving them a visual representation of their ship positions.
- If not satisfied with the ship placement, the player can move any ship by providing its name and new coordinates using the **ship adjustment function**; whereby players are asked whether they are happy with their ships' placement and are given the opportunity to adjust their respective positions.
- Ships are displayed with "O" markers on the player's board, and their positions are also visible on the computer’s guess board during the game, so players can track the computer’s progress.

### Turn-Based Game Loop

- The game alternates between player and computer turns.
- On the hard difficulty, once the computer hits part of a ship, it will continue to guess along the same row or column on its next go until the ship is sunk or a miss occurs.

**Future Improvements**
- One particular feature that would improve the quality and expansiveness of the game is reassigning the 'hard' logic to a new level: 'medium' and establishing logic for hard that uses the same methods in guessing coordinates once a ship has been hit, however instead of randomly choosing a coordinate to start with/after each ship has been sunk the hard level would strategically guess the most likely coordinate for the next ship to be in based on either patterns of play, where it has struck a hit or miss or where the user guesses. 

### Visual Representation of Gameplay

- The player's guess board and the computer's guess board (which shows the player's ship placements) are displayed after each turn.
- Hits are marked with "*", and misses with "X".

---

## Code Examples

Here’s a detailed and comprehensive snippet showcasing two key features of the game: the **ship placement preview** and the **ship adjustment function**, alongside the computer's intelligent **guess logic on *hard* difficulty**.

### Ship Placement Preview:

Each time a player places a ship, the game shows a real-time preview of the current ship layout on the board. This feature ensures that players can visualize their ship positions after every placement, preventing overlap or out-of-bounds errors. Here's how the preview is handled:

```
def place_ship(self, board, ship_size, ship_name):
    while True:
        if board == self.player_board:
            self.display_board_with_ships()  # Show current state of the board with ships
            print(f"\nPlace your {ship_name} (size {ship_size}).")
            print("\nCoordinate system is as follows: top left corner of the board is (0,0) and bottom right corner is (9,9)")
            print("Horizontal ships fill from left (start coordinate) to right & Vertical ships fill from top (start coordinate) down.")
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

```
-**What this adds to the game:**
The player has a clear understanding of where their ships are located on the grid. This feature minimizes errors in ship placement, allowing the player to better strategize their defense against the computer.

### Ship Adjustment Function:
Before starting the guessing phase, players can review their ship layout and adjust any ships they are not satisfied with. This function allows players to move a specific ship to a new location:

```
def review_ship_placement(self):
    while True:
        print("\nYour final ship placement:")
        display_grid(self.player_board)
        happy = input("Are you happy with your ship placement? (yes/no): ").lower()
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

def move_ship(self, ship_name):
    index = list(SHIP_SIZES.keys()).index(ship_name)
    old_coordinates = self.player_ships[index]
    for r, c in old_coordinates:
        self.player_board[r][c] = " "  # Clear old ship position
    size = SHIP_SIZES[ship_name]
    print(f"\nEnter new placement for {ship_name} (size {size}):")
    self.place_ship(self.player_board, size, ship_name)

```
-**What this adds to the game:**
The ship adjustment function gives players more control over their strategy. If they realize that their ship placements are too predictable or vulnerable, they can reposition the ships, improving the defensive aspect of the game.

### Hard Difficulty - Smart Computer Guessing Logic:
The hard difficulty incorporates a smart guessing system where the computer adapts its guesses based on previous hits. Here's the logic for how the computer continues its guesses:

```
def smart_computer_turn(self):
    if self.last_computer_hit and self.last_hit_direction:
        row, col = self.last_computer_hit
        if self.last_hit_direction == "H":
            possible_guesses = [(row, col + 1), (row, col - 1)]
        else:
            possible_guesses = [(row + 1, col), (row - 1, col)]
    elif self.last_computer_hit:
        # If the computer has just registered a hit, it guesses around that hit
        row, col = self.last_computer_hit
        possible_guesses = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        random.shuffle(possible_guesses)  # Add randomness to the guess order
    else:
        # If no hit has been made yet, guess randomly
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
                    print("The computer has sunk one of your ships!")
                    self.last_computer_hit = None  # Reset after sinking a ship
                    self.last_hit_direction = None
                else:
                    # Determine direction of hits for future guesses
                    if self last_hit_direction is None:
                        if r == row:
                            self.last_hit_direction = "H"  # Horizontal direction
                        else:
                            self.last_hit_direction = "V"  # Vertical direction
            else:
                print("Computer missed!")
                self.computer_guesses_board[r][c] = "X"
                if self.last_hit_direction:
                    self.last_hit_direction = None
                break

```

-**What this adds to the game:**
The 'hard' difficulty adds an increased level of competitiveness to the game and uses logical reasoning in attempt to sink the player's ships; making for a more strategic game. 

## Testing
- Tested on multiple browsers, including Chrome and Firefox.
- The game has been tested for responsiveness, ensuring that all messages and inputs are clear across various screen sizes.
- Different difficulty levels were tested to ensure that the computer's logic behaves as expected on both easy and hard modes.
- Initially, errors were presented in running the program whereby the 'player' would be unable to see their ships marked down on the board as means of tracking progress in the game & how close the computer was to winning. However, this was solved by both including a scoreboard which monitors the number of ships sunk by both 'player' and 'computer' as well as also implementing a display of the user's ship placement on the computer's guess board.

## Validator Testing
- **Python**: No syntax errors or issues were found using PEP8 style checking tools.
- **Functionality**: All functions and game logic were tested to ensure proper game flow without crashes.

## Deployment
This game was deployed to Heroku using the following steps:
1. In the GitHub repository, navigate to the **Settings** tab.
2. Under the **Buildpacks** section, set Python as the main buildpack and node.js as the secondary one.
3. Create a `requirements.txt` file listing all necessary Python dependencies.
4. Create a `Procfile` to define the web process.
5. Once these files were in place, the repository was linked to Heroku, and the app was successfully deployed.

[IMG: Heroku Deployment Screenshot]

## Credits
### Content
- Code Institute: Python Essentials course for the general project structure.
- IBM (Qualification): Python for Data Science, AI & Development (hold credential).
- Dr.Codie (YouTube): Used to help understand game logic. 
- BroCode (YouTube): Used to understand necessary commands to deploy smart logic.
- ChatGPT: Assisted with spellcheck and grammar check to improve code readability.

### Media
- N/A (no external media used for this project).


