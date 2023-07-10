import pygame
from pygame.locals import *
import pygame_gui
from UI.combat_menu import CombatMenus
from entities.enemy import Enemy 
import random
from systems.combat_system import CombatSystem



class CombatState:
    def __init__(self, screen, key_pressed, game_manager, enemy):
        self.screen = screen
        self.key_pressed = key_pressed
        self.character = game_manager.character
        self.player_characters = []
        self.player_characters.append(self.character)
        self.player_characters.append(game_manager.companion_1)
        self.player_characters.append(game_manager.companion_2)
        self.player_characters.append(game_manager.companion_3)
        
        

        if enemy != None:
            # Duplicate the enemy object randomly
            num_enemies = random.randint(1, 8)
            self.enemies = [self.duplicate_enemy(enemy) for _ in range(num_enemies)]

            # Get the screen dimensions
            screen_width, screen_height = self.screen.get_size()

            # Calculate the positions for player and enemy rectangles
            player_width, player_height = 50, 50
            enemy_width, enemy_height = 50, 50

            player_x = (screen_width // 4) - (player_width // 2)  # Left side center
            player_y = (screen_height // 6) - (player_height // 1)

            enemy_x = (3 * screen_width // 4) - (enemy_width // 2)  # Right side center
            enemy_y = (screen_height // 4) - (enemy_height * min(num_enemies, 4) // 2)  # Adjusted for vertical positioning

            
            game_manager.character.rect = pygame.Rect(player_x, player_y, player_width, player_height)
            game_manager.companion_1.rect = pygame.Rect(player_x, player_y + 70, 50, 50)
            game_manager.companion_2.rect = pygame.Rect(player_x, player_y + 140, 50, 50)
            game_manager.companion_3.rect = pygame.Rect(player_x, player_y + 210, 50, 50)

            # Render the enemy rectangles (orange)
            self.enemy_rects = []
            num_enemies_per_column = max(min(num_enemies, 8) // 2, 1)  # Ensure at least 1 enemy per column
            for i, enemy in enumerate(self.enemies):
                column_index = i // num_enemies_per_column
                row_index = i % num_enemies_per_column
                enemy_x_offset = column_index * (enemy_width + 10)
                enemy_y_offset = row_index * (enemy_height + 10)
                enemy_rect = pygame.Rect(enemy_x + enemy_x_offset, enemy_y + enemy_y_offset, enemy_width, enemy_height)
                enemy.id_number = i+1
                self.enemy_rects.append(enemy_rect)

            self.combat_menus = \
                CombatMenus(screen, self.player_characters, self.enemies)
            
            self.combat_system = CombatSystem(self.enemies,self.player_characters)

    @staticmethod
    def duplicate_enemy(enemy):
        return Enemy(
            enemy.x, enemy.y, enemy.width, enemy.height,
            enemy.enemy_type
        )


    def get_next_state(self):
        return self.handle_input()
    
    def handle_input(self):

        attack_or_magic_option, entity_selected=self.combat_menus.handle_input()  # Call handle_input method of CombatMenus
        if entity_selected != None:
            # Perform the action using the CombatSystem
            result = self.combat_system.perform_action(attack_or_magic_option, entity_selected)
            if result == 'Flee':
                return 3, True
            print(result)
            
        return None, None



    def update(self):
        pass


    def render(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))

        color_mapping = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0)]

        for i, character in enumerate(self.player_characters):
            if character.alive:
                color = color_mapping[i % len(color_mapping)]  # Select color based on index
                pygame.draw.rect(self.screen, color, character.rect)

        
        for enemy_rect in self.enemy_rects:
            pygame.draw.rect(self.screen, (255, 165, 0), enemy_rect)
        self.combat_menus.render(self.player_characters,self.enemies)  # Call render method of CombatMenus


        #self.combat_menus.render(self.character.health,self.character.magic_points, self.character.name,self.enemies)  # Call render method of CombatMenus












        



