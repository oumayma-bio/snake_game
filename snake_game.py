#!/usr/bin/env python3
import curses
import random
import time
import os

def main(stdscr):
    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    stdscr.timeout(100)  # Refresh rate in ms
    stdscr.keypad(True)  # Enable special keys

    # Get screen dimensions
    height, width = stdscr.getmaxyx()
    
    # Check if the terminal is large enough
    if height < 10 or width < 20:
        try:
            stdscr.clear()
            stdscr.addstr(0, 0, "Terminal too small!")
            if height > 1:
                stdscr.addstr(1, 0, f"Current: {height}x{width}")
            if height > 2:
                stdscr.addstr(2, 0, "Need: 10x20")
            stdscr.refresh()
            stdscr.getch()
        except:
            # If we can't even display the error message, just exit
            pass
        return
    
    # Game variables
    snake = [(height // 2, width // 4)]  # Snake starts as a single segment
    direction = curses.KEY_RIGHT  # Initial direction
    
    # Create initial food
    food = create_food(height, width, snake)
    
    # Score
    score = 0
    
    # Set up borders
    create_border(stdscr, height, width)
    
    # Game Loop
    while True:
        # Display score
        try:
            stdscr.addstr(0, 2, f" SNAKE GAME | Score: {score} | Press 'q' to quit ")
        except curses.error:
            pass
        
        # Draw food
        try:
            stdscr.addch(food[0], food[1], curses.ACS_DIAMOND)
        except curses.error:
            pass
        
        # Draw snake
        for y, x in snake:
            try:
                stdscr.addch(y, x, curses.ACS_CKBOARD)
            except curses.error:
                pass
        
        # Get next key press
        key = stdscr.getch()
        
        # Check for quit
        if key == ord('q'):
            break
        
        # Update direction (only if it's not a 180-degree turn)
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            if key == curses.KEY_UP and direction != curses.KEY_DOWN:
                direction = key
            elif key == curses.KEY_DOWN and direction != curses.KEY_UP:
                direction = key
            elif key == curses.KEY_LEFT and direction != curses.KEY_RIGHT:
                direction = key
            elif key == curses.KEY_RIGHT and direction != curses.KEY_LEFT:
                direction = key
        
        # Calculate new head position
        head = snake[0]
        if direction == curses.KEY_UP:
            new_head = (head[0] - 1, head[1])
        elif direction == curses.KEY_DOWN:
            new_head = (head[0] + 1, head[1])
        elif direction == curses.KEY_LEFT:
            new_head = (head[0], head[1] - 1)
        elif direction == curses.KEY_RIGHT:
            new_head = (head[0], head[1] + 1)
        
        # Add new head to snake
        snake.insert(0, new_head)
        
        # Check if snake has eaten food
        if snake[0] == food:
            # Create new food
            food = create_food(height, width, snake)
            score += 10
            # Speed up the game slightly as score increases
            new_timeout = max(50, 100 - (score // 50) * 5)
            stdscr.timeout(new_timeout)
        else:
            # Remove tail if we didn't eat food
            tail = snake.pop()
            try:
                stdscr.addch(tail[0], tail[1], ' ')
            except curses.error:
                pass
        
        # Check for collisions
        if (
            # Check if snake hit the walls
            snake[0][0] in [0, height-1] or
            snake[0][1] in [0, width-1] or
            # Check if snake hit itself
            snake[0] in snake[1:]
        ):
            game_over(stdscr, height, width, score)
            break
        
        # Refresh the screen
        stdscr.refresh()

def create_food(height, width, snake):
    """Create food at a random position that is not occupied by the snake."""
    # Ensure we have valid dimensions for food placement
    max_height = max(2, height - 2)
    max_width = max(2, width - 2)
    min_height = 1
    min_width = 1
    
    while True:
        food = (random.randint(min_height, max_height), random.randint(min_width, max_width))
        if food not in snake:
            return food

def create_border(stdscr, height, width):
    """Create a border around the game area."""
    # Draw horizontal lines
    for x in range(width-1):
        try:
            stdscr.addch(0, x, curses.ACS_HLINE)
        except curses.error:
            pass
        try:
            stdscr.addch(height-1, x, curses.ACS_HLINE)
        except curses.error:
            pass
    
    # Draw vertical lines
    for y in range(height-1):
        try:
            stdscr.addch(y, 0, curses.ACS_VLINE)
        except curses.error:
            pass
        try:
            stdscr.addch(y, width-1, curses.ACS_VLINE)
        except curses.error:
            pass
    
    # Add corners
    try:
        stdscr.addch(0, 0, curses.ACS_ULCORNER)
    except curses.error:
        pass
    try:
        stdscr.addch(0, width-1, curses.ACS_URCORNER)
    except curses.error:
        pass
    try:
        stdscr.addch(height-1, 0, curses.ACS_LLCORNER)
    except curses.error:
        pass
    try:
        stdscr.addch(height-1, width-1, curses.ACS_LRCORNER)
    except curses.error:
        pass

def game_over(stdscr, height, width, score):
    """Display game over message and final score."""
    stdscr.clear()
    game_over_msg = "GAME OVER!"
    score_msg = f"Your score: {score}"
    exit_msg = "Press any key to exit..."
    
    try:
        stdscr.addstr(height // 2 - 1, (width - len(game_over_msg)) // 2, game_over_msg)
        stdscr.addstr(height // 2, (width - len(score_msg)) // 2, score_msg)
        stdscr.addstr(height // 2 + 1, (width - len(exit_msg)) // 2, exit_msg)
    except curses.error:
        # Fallback if we can't center the text
        try:
            stdscr.addstr(0, 0, game_over_msg)
            stdscr.addstr(1, 0, score_msg)
            stdscr.addstr(2, 0, exit_msg)
        except curses.error:
            pass
    
    stdscr.refresh()
    stdscr.timeout(-1)  # Wait indefinitely for a keypress
    stdscr.getch()

if __name__ == "__main__":
    try:
        # Start curses application
        curses.wrapper(main)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        pass
    finally:
        print("Thanks for playing Snake Game!")
        # Add more information about terminal size requirements
        try:
            terminal_size = os.get_terminal_size()
            print(f"Your terminal size: {terminal_size.columns}x{terminal_size.lines}")
            if terminal_size.lines < 10 or terminal_size.columns < 20:
                print("The game requires a terminal size of at least 10x20.")
                print("Please resize your terminal window and try again.")
        except:
            print("Tip: This game requires a terminal size of at least 10x20.")

