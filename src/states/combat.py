import pygame
from pygame.locals import *
import pygame_gui
from UI.combat_menu import CombatMenus
from entities.enemy import Enemy 
import random

class CombatState:
    def __init__(self, screen, key_pressed, game_manager, enemy):
        self.screen = screen
        self.key_pressed = key_pressed
        self.character = game_manager.character
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
            player_y = (screen_height // 2) - (player_height // 2)

            enemy_x = (3 * screen_width // 4) - (enemy_width // 2)  # Right side center
            enemy_y = (screen_height // 4) - (enemy_height * min(num_enemies, 4) // 2)  # Adjusted for vertical positioning

            # Render the player rectangle (white)
            self.player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

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
                print(enemy.id_number)
                self.enemy_rects.append(enemy_rect)

            self.combat_menus = \
                CombatMenus(screen, self.character.health, self.character.magic_points,self.character.name, self.enemies)


    @staticmethod
    def duplicate_enemy(enemy):
        return Enemy(
            enemy.x, enemy.y, enemy.width, enemy.height,
            enemy.enemy_type, enemy.strength, enemy.weakness, enemy.attack_power
        )


        

    
    def get_next_state(self):
        return self.handle_input()
    
    def handle_input(self):

        

        attack_or_magic_option=self.combat_menus.handle_input()  # Call handle_input method of CombatMenus
        if attack_or_magic_option == 'Flee':
            return 3, True
        if attack_or_magic_option == 'Attack':
            #call combat system
            pass
        if attack_or_magic_option == 'Fire':
            #call combat system
            pass
        if attack_or_magic_option == 'Water':
            print("Water")

        

        return None, None



    def update(self):
        pass


    def render(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))


        pygame.draw.rect(self.screen, (255, 255, 255), self.player_rect)



        for enemy_rect in self.enemy_rects:
            pygame.draw.rect(self.screen, (255, 165, 0), enemy_rect)






        self.combat_menus.render(self.character.health,self.character.magic_points, self.character.name,self.enemies)  # Call render method of CombatMenus












        



