import pygame
from pygame.locals import *
import pygame_gui
from UI.combat_menu import CombatMenus


class CombatState:
    def __init__(self, screen, key_pressed, character, enemy):
        self.screen = screen
        self.key_pressed = key_pressed
        self.character = character
        self.enemy = enemy
        self.combat_menus = CombatMenus(screen)  # Create an instance of CombatMenus

        
        

    
    def get_next_state(self):
        return self.handle_input()
    
    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[K_q]:
            return 3, True  # Exit combat state

        self.combat_menus.handle_input()  # Call handle_input method of CombatMenus

        

        return None, None



    def update(self):
        pass


    def render(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))
        self.combat_menus.render()  # Call render method of CombatMenus


        # Get the screen dimensions
        screen_width, screen_height = self.screen.get_size()

        # Calculate the positions for player and enemy rectangles
        player_width, player_height = 50, 50
        enemy_width, enemy_height = 50, 50

        player_x = (screen_width // 4) - (player_width // 2)  # Left side center
        player_y = (screen_height // 2) - (player_height // 2)

        enemy_x = (3 * screen_width // 4) - (enemy_width // 2)  # Right side center
        enemy_y = (screen_height // 2) - (enemy_height // 2)

        # Render the player rectangle (white)
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        pygame.draw.rect(self.screen, (255, 255, 255), player_rect)

        # Render the enemy rectangle (orange)
        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        pygame.draw.rect(self.screen, (255, 165, 0), enemy_rect)








        



