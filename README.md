# Snake Game

A classic Snake game implementation in Python using the curses library for terminal-based gameplay.

![Snake Game](https://github.com/oumayma-bio/snake_game/raw/main/screenshot.png)

## Description

This is a terminal-based implementation of the classic Snake game. The player controls a snake that moves around the screen, eating food to grow longer. The game ends if the snake runs into the border or itself.

## Features

- Terminal-based gameplay with curses library
- Arrow key controls for snake movement
- Score tracking
- Game over screen with final score
- Terminal size validation
- Border display
- Simple and intuitive gameplay

## Requirements

- Python 3.x
- curses library (included in standard Python library on Unix/Linux/macOS)
- For Windows users: `windows-curses` package

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/oumayma-bio/snake_game.git
   cd snake_game
   ```

2. For Windows users only, install the windows-curses package:
   ```
   pip install windows-curses
   ```

## How to Play

1. Run the game:
   ```
   python snake_game.py
   ```

2. Controls:
   - Arrow keys: Change direction of the snake
   - Q: Quit the game

3. Gameplay:
   - Guide the snake to eat the food (◆)
   - Each food eaten increases your score and makes the snake longer
   - Avoid hitting the borders or the snake's own body

## Development

This project is open for contributions. Feel free to fork the repository and submit pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

- Oumayma Alhou 