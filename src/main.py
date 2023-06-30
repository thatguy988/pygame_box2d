import pygame
from pygame.locals import *
from enum import Enum
from states.mainmenu import MainMenuState
from states.platforming import PlatformingState
from leveldata import load_level_data




# State enumeration
class GameState(Enum):
    MAIN_MENU = 1
    PAUSE_MENU = 2
    PLATFORMING = 3

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("State Machine Game")

# Game variables
state_stack = [GameState.MAIN_MENU]
running = True

# Create state instances dictionary
state_instances = {
    GameState.MAIN_MENU: MainMenuState(screen),
    GameState.PLATFORMING: PlatformingState(screen, 1)
}

# Main game loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    current_state = state_stack[-1]  # Get the current state from the top of the stack
    state_instance = state_instances[current_state]

    # Update game logic based on current state
    state_instance.update()
    screen.fill((0, 0, 0))  # Clear the screen
    state_instance.render()

    # Handle state transitions
    next_state = state_instance.get_next_state()  # Method in state instance to get the next state
    
    if next_state is not None:
        if next_state == 1:
            state_stack = [GameState.MAIN_MENU]  # Reset the state stack
        elif next_state == 3:
            state_stack.append(GameState.PLATFORMING)  # Push the next state onto the stack

    pygame.display.flip()  # Update the display

# Quit the game
pygame.quit()



