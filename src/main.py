import pygame
from pygame.locals import *
from enum import Enum
from states.mainmenu import MainMenuState
from states.platforming import PlatformingState
from states.pausemenu import PauseMenuState
from states.combat import CombatState

from game_manager import GameManager


# State enumeration
class GameState(Enum):
    MAIN_MENU = 1
    PAUSE_MENU = 2
    PLATFORMING = 3
    COMBAT = 4

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("State Machine Game")

# Game variables
state_stack = [GameState.MAIN_MENU]
running = True
key_pressed = False

game_manager= GameManager()

# Create state instances dictionary
state_instances = {
    GameState.MAIN_MENU: MainMenuState(screen, key_pressed, game_manager),
    GameState.PAUSE_MENU: PauseMenuState(screen, key_pressed, game_manager),
    GameState.PLATFORMING: PlatformingState(screen, 1, key_pressed,game_manager),
    GameState.COMBAT:CombatState(screen, key_pressed, None, None, game_manager)
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
    

    #  Handle state transitions
    if current_state == GameState.PLATFORMING:
        next_state, key_pressed, character, enemy = state_instance.get_next_state()
    else:
        next_state, key_pressed = state_instance.get_next_state()
    

    if next_state is not None:
        if next_state == 1:
            if GameState.MAIN_MENU not in state_stack:
                state_stack = [GameState.MAIN_MENU]  # start the state stack with main menu
            else:
                # return to main menu from platforming state
                state_stack.pop() #remove pause menu
                state_stack.pop() #remove platforming state
                state_instances[GameState.MAIN_MENU] = MainMenuState(screen, key_pressed, game_manager)
        elif next_state == 2:
            if GameState.PAUSE_MENU not in state_stack:
                state_stack.append(GameState.PAUSE_MENU)
                state_instances[GameState.PAUSE_MENU] = PauseMenuState(screen, key_pressed,game_manager)
        elif next_state == 3:
            if GameState.PLATFORMING not in state_stack:
                state_instances[GameState.PLATFORMING] = PlatformingState(screen, 1, key_pressed, game_manager)  # Reset the state instance
                state_stack.append(GameState.PLATFORMING)  # Push the next state onto the stack
            else:
                state_stack.pop()# pop pause menu, combat go back to current platforming state from combat or pause menu state
        elif next_state == 4:
            #from platforming state to combat state
            if GameState.COMBAT not in state_stack:
                state_instances[GameState.COMBAT] = CombatState(screen,key_pressed,character,enemy, game_manager)  # Reset the state instance
                state_stack.append(GameState.COMBAT)

    
    pygame.display.flip()  # Update the display


pygame.quit()



