import pygame
from pygame.locals import *
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
            num_enemies = random.randint(3, 5)
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
                enemy.rect = enemy_rect

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
        
        self.combat_system.check_if_all_enemies_dead()
        self.combat_system.check_if_all_player_characters_dead()
        if self.combat_system.battle_succesful:
            [character.restore_health_and_magic() for character in self.player_characters]
            return 3, True
        if self.combat_system.game_over:
            return 1, True

        if(self.combat_system.players_turn):
            if(self.combat_system.check_if_players_turn()):
                character_taking_action = self.player_characters[self.combat_system.player_index]
                while(not character_taking_action.alive):
                    self.combat_system.player_index += 1
                    if(self.combat_system.player_index == len(self.player_characters)):
                        self.combat_system.player_index = 0
                    character_taking_action = self.player_characters[self.combat_system.player_index]

                attack_or_magic_option, entity_selected=self.combat_menus.handle_input()  # Call handle_input method of CombatMenus
                if entity_selected != None:
                    # Perform the action using the CombatSystem
                    result = self.combat_system.perform_action(attack_or_magic_option, entity_selected,character_taking_action)
                    if result == 'Flee':
                        return 3, True
                    if attack_or_magic_option != 'Flee':
                        Redraw = self.combat_system.check_if_alive(entity_selected)
                        if Redraw == False:
                            self.combat_menus.enemy_dead(self.combat_system.enemies)
                            self.combat_system.reorganize()
                            Redraw = True
                        
                    self.combat_system.player_index += 1
                    if(self.combat_system.player_index == len(self.player_characters)):
                        self.combat_system.player_index = 0
               
            else:
                self.combat_system.num_turns_enemies = self.combat_system.calculate_num_turns(self.enemies)
                self.combat_system.players_turn = False
                self.combat_system.enemy_index = 0
        else:
            if(self.combat_system.check_if_enemies_turn()):
                enemy_taking_action = self.combat_system.enemies[self.combat_system.enemy_index]
                while(not enemy_taking_action.alive):
                    self.combat_system.enemy_index += 1
                    if(self.combat_system.enemy_index == len(self.combat_system.enemies)):
                        self.combat_system.player_index = 0
                    enemy_taking_action = self.combat_system.enemies[self.combat_system.enemy_index]

                attack_or_magic_option, entity_selected=self.combat_system.handle_enemy_input()
                self.combat_system.enemy_perform_action(attack_or_magic_option,entity_selected, enemy_taking_action)
                self.combat_system.check_if_alive(entity_selected)
                
                self.combat_system.enemy_index += 1
                if(self.combat_system.enemy_index == len(self.combat_system.enemies)):
                    self.combat_system.enemy_index = 0
            else:
                self.combat_system.num_turns_player = self.combat_system.calculate_num_turns(self.player_characters)
                self.combat_system.players_turn = True
                self.combat_system.player_index = 0
                
        if(self.combat_system.game_over == True):
            return 3, True

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

        for i, enemy in enumerate(self.combat_system.enemies):
            if enemy.alive:
                pygame.draw.rect(self.screen, (255, 165, 0), enemy.rect)
        self.combat_menus.render(self.player_characters,self.combat_system.enemies,
                                 self.combat_system.num_turns_player,
                                 self.player_characters[self.combat_system.player_index])  # Call render method of CombatMenus

        