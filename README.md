# Battleships Game

Battleships is a Python terminal game that reimagines the classic Battleships experience in a text-based interface. The game is designed to run on a terminal that is 80 characters wide and 24 rows high, ensuring that every message and prompt remains clearly visible without scrolling. The game is deployed on Heroku and can be played live.


[Here is a live version of the project - Click to Play!](https://battleships-ktp8-26036706a071.herokuapp.com)
(Run on Google Chrome if Safari/FireFox privacy settings mitigate run)


![Screenshot 2024-10-12 at 20 47 53](https://github.com/user-attachments/assets/d4d3e8fb-81d9-44a4-9ea1-ca893c3153a6)

---


## Table of Contents

1. [Introduction](#introduction)
2. [Game Rules](#game-rules)
3. [Technologies Used](#technologies-used)
4. [Features](#features)
    - [Core Gameplay](#core-gameplay)
    - [Incremental Stage-Based Interaction](#incremental-stage-based-interaction)
5. [Game Logic Details](#game-logic-details)
    - [Easy vs. Hard Mode](#easy-vs-hard-mode)
    - [Key Code Snippets](#key-code-snippets)
6. [Automated Testing](#automated-testing)
7. [Manual Testing](#manual-testing)
8. [Initial Project and Git History](#initial-project-and-git-history)
9. [Possible Improvements](#possible-improvements)
10. [Deployment](#deployment)
11. [Credits](#credits)

---

## Introduction

Battleships is a command-line game developed entirely in Python. In this game, the player places their ships on a 10x10 grid and then alternates turns with a computer opponent to locate and sink each other's ships. The game includes two difficulty levels—Easy and Hard—with distinct computer strategies. The design also emphasizes a step-by-step interface that pauses between each stage of the game, so that all messages and outcomes remain visible on a terminal limited to 80×24 characters.

---


## Game Rules

- **Ship Types:**  
  Each player (both the human and computer) has five types of ships:
  - **Carrier:** occupies 5 cells.
  - **Battleship:** occupies 4 cells.
  - **Cruiser:** occupies 3 cells.
  - **Submarine:** occupies 3 cells.
  - **Destroyer:** occupies 2 cells.
  
- **Ship Placement:**  
  Players are prompted to place each ship by entering coordinates and selecting an orientation (horizontal or vertical). A preview of the board is displayed after every placement to help avoid overlaps and out-of-bound errors. Players can review and adjust ship placements before starting the game.

- **Turn-Based Play:**  
  After placement, players alternate turns. On each turn:
  - The player enters a guess (a coordinate pair).
  - If a guess hits a ship, a "Hit!" message is displayed, and the cell is marked with "*".
  - If the guess misses, "Miss!" is printed, and the cell is marked with "X".
  - If the same coordinate is guessed twice, a special message is displayed:
    > "Unlucky! You've already taken a shot there - what a waste of a go! Unfortunately, the game must go on..."
  
- **Game Flow:**  
  The game pauses between key actions so that all feedback remains visible on the 80×24 terminal. Prompts ensure that after each turn, the user must press Enter to view the scoreboard, then proceed to the computer’s turn, and finally see the updated boards before starting the next turn.

- **Winning the Game:**  
  The game ends when either the player or the computer sinks all of the opponent’s ships. The final scoreboard is displayed to show the outcome.

---


## Technologies Used

- **Python 3.12.2** – Primary programming language.
- **Heroku** – Deployment platform.
- **Git** – Version control system.
- **VS Code & Gitpod** – Development environments.
- **unittest** – Automated testing framework.
- **flake8** – PEP8 code style checker.

---


## Features

### Core Gameplay

- **Ship Placement and Adjustment:**  
  Players place their ships with real-time board previews. The game prevents invalid placements (overlap or out-of-bound coordinates) and allows players to adjust ship positions before the game begins.

- **Turn-Based Game Loop with Incremental Interaction:**  
  The game pauses between stages to ensure every message is visible. After a guess, the game waits for a confirmation (Enter key) before displaying the scoreboard, proceeding to the computer’s turn, and then showing updated guess boards.

- **Dynamic Feedback:**  
  The game provides immediate feedback on every action:
  - **Hit!** or **Miss!** messages.
  - Duplicate guesses are flagged with a humorous message.
  - Clear instructions are provided if the input is invalid.

### Incremental Stage-Based Interaction

- The interface is designed so that the player controls the pace:
  - After making a guess, the player sees the result and then presses Enter to view the scoreboard.
  - A subsequent prompt tells the player to press Enter to allow the computer to take its turn.
  - After the computer's turn, the updated boards are shown only after the player presses Enter.
  - This ensures that messages do not scroll off the screen on a small terminal.

---


## Game Logic Details

### Easy vs. Hard Mode

- **Easy Mode:**  
  In easy mode, the computer makes random guesses. This mode is straightforward and serves as an introduction for beginners.

- **Hard Mode:**  
  Hard mode uses a more strategic approach:
  - When the computer hits a ship, it remembers the last hit location.
  - The computer then continues to guess adjacent cells (either horizontally or vertically) until the ship is sunk or a miss is recorded.
  - The logic uses variables such as `last_computer_hit` and `last_hit_direction` to determine the next best guess.
  
### Key Code Snippets

**Incremental Prompting:**

```
print("\nPress Enter to view the scoreboard and proceed to the computer's turn.")
wait_for_enter("Press Enter to continue: ")
```
_This snippet shows how the game pauses after a player's guess, ensuring that feedback remains on screen._

**Duplicate Guess Selection:** 

```
if guesses_board[row][col] != " ":
    print("Unlucky! You've already taken a shot there - what a waste of a go! "
          "Unfortunately, the game must go on...")
    return "duplicate"
```
_This code checks if a coordinate has een guessed before and displays a special message if so._

**Computer's Hard Mode Logic:**

```
if self.last_computer_hit and self.last_hit_direction:
    row, col = self.last_computer_hit
    if self.last_hit_direction == "H":
        possible_guesses = [(row, col + 1), (row, col - 1)]
    else:
        possible_guesses = [(row + 1, col), (row - 1, col)]
elif self.last_computer_hit:
    row, col = self.last_computer_hit
    possible_guesses = [(row + 1, col), (row - 1, col),
                        (row, col + 1), (row, col - 1)]
    random.shuffle(possible_guesses)
```
_This logic enables the computer to pursue a strategic follow-up after a hit in hard-mode._

---


## Automated Testing

Automated unit tests were implemented using Python’s unittest module. The tests cover critical functions such as grid creation, guess validation, and ship sinking logic. A screenshot of the test results is included below:

Tests can be run with:

```
python -m unittest discover
```
_This command searches for and executes all tes cases in files with names beginning wth **test**._

![Automated Test Screenshot](https://imgur.com/CecsNch.png)

---


## Manual Testing

Manual testing was conducted to verify robust handling of all potential errors:

**Coordinate Input:**
- Tested valid inputs (e.g., "3,4") and invalid ones (non-numeric, out-of-bound, empty input).

**Name Input:**
- Tested for blank names, ensuring that the message "Name cannot be blank. Please enter your name." is displayed.

**Guess Validation:**
- Verified that invalid inputs (empty, non-numeric, out-of-bound) prompt appropriate error messages.
- Confirmed that repeated guesses yield the duplicate guess message.

**Incremental Prompts:**
- Checked that the game pauses at the right moments and only proceeds when Enter is pressed.

_Screenshots of manual testing examples are provided:_

- ![Manual Test - Name Input](https://imgur.com/9PEuvYM.png)
_Name Input_

- ![Manual Test - Coordinate Input](https://imgur.com/HUwiWku.png)
_Coordinate Input Validation_

- ![Manual Test - Stage Prompts](https://imgur.com/Bqdeojc.png)
- ![Manual Test - Stage Prompts](https://imgur.com/htthoW3.png)
_Stage Prompts to Confirm Next Stage_

- ![Manual Test - Duplicate Guess](https://imgur.com/RjowqTz.png)
_Duplicate Guesses_

---


## Initial Project and Git History

The project was initially started in an incorrect framework, resulting in an incomplete commit history. The project was then restructured and the code was imported in chunks to form the final version. The early commits are available in the original repository:

**Original Repo:**  
[Original Repo](https://github.com/KTP8/Battleships)

_Screenshots of the original commit history:_

![Screenshot 2024-10-12 at 20 49 18](https://github.com/user-attachments/assets/7ec1b6fb-f461-4ea8-b21b-b7d911fde652)
![Screenshot 2024-10-12 at 20 49 49](https://github.com/user-attachments/assets/b98c9572-60ee-4de7-805b-33e9a3313034)
![Screenshot 2024-10-12 at 20 50 09](https://github.com/user-attachments/assets/925a4f25-0119-4376-a323-fed52eff42dc)
![Screenshot 2024-10-12 at 20 50 23](https://github.com/user-attachments/assets/edaf75c1-a766-47b2-ab95-8645a1e4776b)

_There are a limited number of commits for this project, and it may appear that the project was completed in a short period. However, this was due to the use of an incorrect template initially, which led to restarting the project in the correct format. I subsequently copied over my original code from my original workspace: github.com/ktp8/battleships in chunks. Despite the limited commits, the project was developed over ample time, and all code is original and not plagiarised._

---


## Possible Improvements

Potential future improvements include:

**Additional Difficulty Level:**
- Introduce a "Medium" level with refined logic that blends random guessing with strategy. The computer could collect data on frequently played moves and use machine learning techniques to predict the player's ship placements, with varying accuracy based on difficulty.

**Enhanced AI:**
- Improve the computer’s decision-making by analyzing patterns in previous moves. For example, by tracking hit/miss ratios and adapting guessing strategies accordingly, the computer's performance could be fine-tuned.

**Graphical User Interface:**
- Create a graphical version using PyGame to enhance user interaction.

**Color-Coded Output:**
- Use a library like colorama to add color to hits, misses, and ship placements for better visual clarity.

**GitHub Actions Workflow:**
- Set up a GitHub Actions workflow to automatically run unit tests on each push to GitHub, ensuring continuous integration and catching bugs early.

---


## Deployment

Battleships is deployed on Heroku. The deployment process involved:

- Creating a `requirements.txt` file with all dependencies.
- Setting up a `Procfile` to define the web process.
- Configuring the appropriate buildpacks (Python as primary, Node.js as secondary for terminal emulation if needed).
- Linking the GitHub repository to Heroku and deploying the app.
- Verifying that the app runs as expected.

![Deployment Screenshot](https://imgur.com/3OqX5Cj.png)
![Working App](https://imgur.com/b54KU8G.png)

---


## Credits

**Development:**  
The Battleships game is an original project developed in Python. The design and code are entirely original, built from scratch using lessons from various educational resources and online tutorials.

**Resources and Inspirations:**  
- Concepts and best practices were drawn from the Python Essentials course, YouTube, Precipio & ChatGPT loop concepts.
- Tutorials and articles on terminal game development and automated testing contributed to shaping the project.
- Various online communities and documentation (e.g., Python docs, GitHub Actions documentation) were referenced during development.

**Media and Assets:**  
All images and screenshots used in this README are either original or have been properly attributed.

Battleships is a robust terminal game that combines strategic gameplay with a user-friendly, stage-based interface. The project has undergone extensive automated and manual testing, and further improvements are planned to refine the game logic and user experience.


