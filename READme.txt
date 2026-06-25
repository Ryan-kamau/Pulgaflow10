# Number Guesser Game 🎮

A multiplayer number guessing game built with Python and Tkinter. Players take turns guessing a randomly generated number within a selected range. The game supports multiple players and a customizable number range.

## Features

* Multiplayer support (minimum 2 players)
* Custom player names
* Custom number range selection
* Turn-based gameplay
* Input validation
* Automatic window resizing (opens at half the screen size)
* Keyboard support (`Enter` key shortcuts)
* Displays hints:

  * Too high
  * Too low
* Announces the winner

---

## Screenshots

You can add screenshots here later:

* Player setup screen
* Name input screen
* Game screen
* Winning screen

---

## Requirements

Make sure Python is installed on your machine.

Python version:

```bash
Python 3.x
```

Required libraries:

```python
tkinter
random
```

`random` comes built into Python.

Tkinter is usually included with Python installations.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/number-guesser.git
```

Move into the project folder:

```bash
cd number-guesser
```

Run the application:

```bash
python main.py
```

---

## How to Play

### Step 1: Choose number of players

Enter the number of players.

Requirements:

* Minimum of 2 players

---

### Step 2: Enter player names

Type each player's name.

Example:

```text
Player 1: Ryan
Player 2: John
Player 3: Sarah
```

---

### Step 3: Select a range

Choose the minimum and maximum values.

Example:

```text
Min: 1
Max: 100
```

The game will generate a random number within that range.

---

### Step 4: Start the game

Click:

```text
Start Game
```

---

### Step 5: Take turns guessing

Players guess one at a time.

Hints will appear:

```text
Ryan, that's too low.
John's turn.
```

or

```text
Sarah, that's too high.
Ryan's turn.
```

---

### Step 6: Win the game

When a player guesses correctly:

```text
Ryan Congratulations you won!!
```

The game ends automatically.

---

## Project Structure

```text
number-guesser/
│
├── main.py
├── README.md
```

---

## Technologies Used

* Python
* Tkinter GUI toolkit
* Random module

---

## Future Improvements

Possible features that could be added:

* Restart game button
* Score tracking
* Difficulty levels
* Timer countdown
* Leaderboard
* Sound effects
* Dark mode
* Maximum attempts option

---

## Author

Created by Ryan 🚀
