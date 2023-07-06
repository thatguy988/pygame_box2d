import pygame


from pygame.locals import *
from Box2D import *


BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
tile_size = 64

class PlatformingState:
    def __init__(self, screen, level_id, key_pressed, game_manager):
        self.game_manager = game_manager
        self.game_manager.initialize_platforming_state(screen,level_id,key_pressed)
    
    def get_next_state(self):
        return self.handle_input()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[K_p]:
            self.game_manager.key_pressed = True
            return 2, self.game_manager.key_pressed, None , None

        
        
        if self.game_manager.npc_talk is not None:
            if not self.game_manager.text_render:
                if keys[K_f] and not self.game_manager.key_pressed:
                    self.game_manager.text_render = True  # Show NPC dialogue
                    self.game_manager.key_pressed = True  # Set the key press flag to True
            else:
                if keys[K_f] and not self.game_manager.key_pressed:
                    self.game_manager.text_render = False  # Hide NPC dialogue
                    self.game_manager.key_pressed = True  # Set the key press flag to True
                elif not keys[K_f]:
                    self.game_manager.key_pressed = False  # Reset the key press flag to False

        # Reset the key press flag to False if the "F" key is not being pressed
        if not keys[K_f]:
            self.game_manager.key_pressed = False


        combat_state_check, enemy = \
            self.game_manager.collision.check_collision(self.game_manager.enemies, self.game_manager.enemies_physical_body,
                                                        self.game_manager.character, self.game_manager.character_physical_body, 
                                                        self.game_manager.world)

        self.game_manager.is_jumping = \
              self.game_manager.movement.player_movement(keys, self.game_manager.character_physical_body, self.game_manager.is_jumping)
        
        if combat_state_check == 4:
            self.game_manager.key_pressed = True
            return combat_state_check, self.game_manager.key_pressed, self.game_manager.character, enemy
        else:
            return None, self.game_manager.key_pressed, None, None  # No state transition
    


    def update(self):
        time_step = 1.0 / 60.0  # Update time step (60 FPS)
        velocity_iterations = 6  # Velocity iterations for physics solver
        position_iterations = 2  # Position iterations for physics solver
        self.game_manager.world.Step(time_step, velocity_iterations, position_iterations)

        self.game_manager.character.move(self.game_manager.character_physical_body)
        self.game_manager.npc_talk = \
            self.game_manager.collision.npc_collision(self.game_manager.npcs, self.game_manager.npcs_physical_body, 
                                                      self.game_manager.character, self.game_manager.character_physical_body,
                                                      self.game_manager.textbox)
        
        self.game_manager.movement.enemy_movement(self.game_manager.enemies, self.game_manager.enemies_physical_body, 
                                                  self.game_manager.direction_timer, self.game_manager.direction_change_interval, 
                                                  time_step)

        self.game_manager.is_jumping = \
            self.game_manager.collision.tile_character_collision(self.game_manager.character, self.game_manager.character_physical_body,
                                                                  self.game_manager.tile_physical_bodies, self.game_manager.is_jumping, 
                                                                  tile_size)
        

        self.game_manager.camera.update(self.game_manager.character)

        self.game_manager.load_next_node()

    def construct_game_objects(self):
        game_objects = []

        # Add tiles to game_objects
        game_objects += [(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size), BLUE) for y, row in enumerate(self.game_manager.level_data) for x, tile in enumerate(row) if tile == 1]

        # Add NPCs to game_objects
        game_objects += [(pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size), (255, 165, 255)) for y, row in enumerate(self.game_manager.level_data) for x, tile in enumerate(row) if tile == 11]

        # Add enemies to game_objects
        game_objects += [(pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height), (255, 165, 0)) for enemy in self.game_manager.enemies]

        # Add character to game_objects
        game_objects.append((pygame.Rect(self.game_manager.character.x, self.game_manager.character.y, self.game_manager.character.width, self.game_manager.character.height), WHITE))

        return game_objects

    def render(self):
        # Construct the game_objects list
        game_objects = self.construct_game_objects()

        # Render the camera view
        self.game_manager.camera.render(game_objects)

        if self.game_manager.text_render:
            delta_time = self.game_manager.clock.tick(60) / 1000.0  # Assuming 60 FPS as the desired frame rate

            self.game_manager.textbox.container.rect.center = (150, 100)  # Adjust the position of the text box container
            self.game_manager.textbox.container.update(delta_time)
            self.game_manager.textbox.textbox.update(delta_time)
            text_surface = self.game_manager.textbox.font.render(self.game_manager.textbox.text, True, self.game_manager.textbox.color)
            self.game_manager.screen.blit(text_surface, self.game_manager.textbox.position)




        # game_objects = []
        # for y, row in enumerate(self.game_manager.level_data):
        #     for x, tile in enumerate(row):
        #         if tile == 1:
        #             tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        #             game_objects.append((tile_rect, BLUE))
        #         elif tile == 11:
        #             npc_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
        #             game_objects.append((npc_rect, (255, 165, 255)))

        # for enemy in self.game_manager.enemies:
        #     enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
        #     game_objects.append((enemy_rect, (255, 165, 0)))

        # character_rect = pygame.Rect(self.game_manager.character.x, self.game_manager.character.y, self.game_manager.character.width, self.game_manager.character.height)
        # game_objects.append((character_rect, WHITE))

