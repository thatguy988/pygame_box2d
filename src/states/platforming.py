import pygame
import random

from pygame.locals import *
from Box2D import *


from entities.character import Character
from entities.enemy import Enemy 
from entities.npc import NPC
from leveldata.level_1 import load_level_data, get_node_id
from systems.collision import CollisionSystem 
from systems.movement import MovementSystem
from camera import Camera
from UI.textbox import TextBox
from pygame_gui import UIManager



BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
tile_size = 64

class PlatformingState:
    def __init__(self, screen, level_id, key_pressed):
        self.enemies = []
        self.enemies_body = []
        self.tile_bodies = []
        self.npcs = []
        self.npcs_body = []
        self.screen = screen
        tile_size = 64  # Adjust the size of the tile as needed
        self.exit_direction = None  # Initialize exit direction variable
        self.level_id=level_id
        self.level_data = load_level_data(self.level_id)
        self.camera_speed = 0.25
        self.level_width = len(self.level_data[0]) * tile_size  # Calculate the level width based on the tile size
        self.level_height = len(self.level_data) * tile_size # Calculate the level height based on the tile size
        player_position = self.find_player_position()
        self.character = Character.create_character(player_position[0] * tile_size, player_position[1] * tile_size)
        self.is_jumping = False  # Variable to track jump state
        self.direction_change_interval = 20.0  # Time interval for changing direction (in seconds)
        self.direction_timer = 0.0  # Timer to keep track of time passed
        self.collision = CollisionSystem()
        self.movement = MovementSystem()
        self.ui_manager = UIManager((screen.get_width(), screen.get_height()))

        #self.textbox = TextBox((50, 50), (200, 100), pygame.font.Font(None, 24), pygame.Color("white"))
        self.textbox = TextBox((50, 50), (200, 100), pygame.font.Font(None, 24), pygame.Color("white"), self.ui_manager)
        self.clock= pygame.time.Clock()

        

        self.npc_talk = False
        self.text_render = False
        self.key_pressed = key_pressed
        self.camera = Camera(self.screen, self.level_width, self.level_height, self.camera_speed)


        # Create a Box2D world
        self.world = b2World(gravity=(0, 10), doSleep=True)

        # Create static bodies for the blue tiles
        for y, row in enumerate(self.level_data):
            for x, tile in enumerate(row):
                if tile == 1:
                    tile_body = self.world.CreateStaticBody(
                        position=(x * tile_size, y * tile_size),
                        shapes=b2PolygonShape(box=(tile_size / 2 , tile_size / 2))
                    )
                    self.tile_bodies.append(tile_body)
                elif tile == 7:  # Spawn enemy at tile with value 7
                    enemy = Enemy.create_enemy(x *tile_size, y *tile_size, "slime")
                    enemy_body = self.world.CreateDynamicBody(
                        position=(x * tile_size, y * tile_size),
                        shapes=b2PolygonShape(box=(enemy.width / 2, enemy.height / 2)),
                        linearDamping=0.5,
                        angularDamping=0.5
                    )
                    self.enemies.append(enemy)  # Add enemy to a list
                    self.enemies_body.append(enemy_body) #add enemy body to a list
                elif tile == 10:
                    invisible_tile_body = self.world.CreateStaticBody(
                        position=(x * tile_size, y * tile_size),
                        shapes=b2PolygonShape(box=(tile_size / 2 , tile_size / 2))
                    )
                elif tile == 11:
                    npc = NPC(x * tile_size, y * tile_size, 50, 50, ["Hello, there!", "How are you?", "Nice weather today!"])

                    npc_body = self.world.CreateStaticBody(
                        position=(x * tile_size, y * tile_size),
                        shapes=b2PolygonShape(box=(tile_size / 2 , tile_size / 2))
                    )
                    self.npcs.append(npc)
                    self.npcs_body.append(npc_body)
                    
        # Create a dynamic character body
        self.character_body = self.world.CreateDynamicBody(
            position=(player_position[0]*tile_size, player_position[1]*tile_size),
            shapes=b2PolygonShape(box=(self.character.width / 2 , self.character.height / 2)),
            linearDamping=0.5,
            angularDamping=0.5
        )
        

    def get_next_state(self):
        return self.handle_input()
    
    def find_player_position(self):
        for y, row in enumerate(self.level_data):
            for x, tile in enumerate(row):
                if tile == 2:
                    return (x, y)
        return (0, 0)  # Default to (0, 0) if no player position is found
    
    def update_player_position(self, exit_direction):
        tile_mapping = {
            "right": 3,
            "left": 4,
            "up": 5,
            "down": 6
        }

        player_position = None
        target_tile = tile_mapping.get(exit_direction)

        if target_tile is not None:
            for y, row in enumerate(self.level_data):
                for x, tile in enumerate(row):
                    if tile == target_tile:
                        player_position = (x, y)
                        break

        if player_position is not None:
            # Reset the Box2D body position for the character
            self.character_body.position = b2Vec2(player_position[0] * tile_size, player_position[1] * tile_size)


    def handle_input(self):
        keys = pygame.key.get_pressed()
        

        if keys[K_p]:
            self.key_pressed = True
            return 2, self.key_pressed, None , None

        
        
        if self.npc_talk is not None:
            if not self.text_render:
                if keys[K_f] and not self.key_pressed:
                    self.text_render = True  # Show NPC dialogue
                    self.key_pressed = True  # Set the key press flag to True
            else:
                if keys[K_f] and not self.key_pressed:
                    self.text_render = False  # Hide NPC dialogue
                    self.key_pressed = True  # Set the key press flag to True
                elif not keys[K_f]:
                    self.key_pressed = False  # Reset the key press flag to False

        # Reset the key press flag to False if the "F" key is not being pressed
        if not keys[K_f]:
            self.key_pressed = False


        combat_state_check, enemy =self.collision.check_collision(self.enemies, self.enemies_body,self.character, self.character_body, self.world)

        

        
        
        self.is_jumping = self.movement.player_movement(keys, self.character_body, self.is_jumping)
        if combat_state_check == 4:
            self.key_pressed = True
            return combat_state_check, self.key_pressed, self.character, enemy
        else:
            return None, self.key_pressed, None, None  # No state transition
    
    def out_of_bounds_check(self):
        # Check if the character is out of bounds
        if self.character.x < 0:
            self.exit_direction = "left"
            return True
        elif self.character.x > self.level_width:
            self.exit_direction = "right"
            return True
        elif self.character.y < 0:
            self.exit_direction = "up"
            return True
        elif self.character.y > self.level_height:
            self.exit_direction = "down"
            return True

    def update(self):
        time_step = 1.0 / 60.0  # Update time step (60 FPS)
        velocity_iterations = 6  # Velocity iterations for physics solver
        position_iterations = 2  # Position iterations for physics solver
        self.world.Step(time_step, velocity_iterations, position_iterations)

        self.character.move(self.character_body)
        #combat_state_check=self.collision.check_collision(self.enemies, self.enemies_body,self.character, self.character_body, self.world)
        self.npc_talk = self.collision.npc_collision(self.npcs, self.npcs_body, self.character, self.character_body,self.textbox)
        self.movement.enemy_movement(self.enemies, self.enemies_body, self.direction_timer, self.direction_change_interval, time_step)

        self.is_jumping = self.collision.tile_character_collision(self.character, self.character_body, self.tile_bodies, self.is_jumping, tile_size)
        

        self.camera.update(self.character)

        self.load_next_node()



        

        

    def render(self):
        


        # Render the game objects using the camera
        game_objects = []
        for y, row in enumerate(self.level_data):
            for x, tile in enumerate(row):
                if tile == 1:
                    tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    game_objects.append((tile_rect, BLUE))
                elif tile == 11:
                    npc_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                    game_objects.append((npc_rect, (255, 165, 255)))

        for enemy in self.enemies:
            enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
            game_objects.append((enemy_rect, (255, 165, 0)))

        character_rect = pygame.Rect(self.character.x, self.character.y, self.character.width, self.character.height)
        game_objects.append((character_rect, WHITE))

        # Render the camera view
        self.camera.render(game_objects)

        
        if self.text_render:
            delta_time = self.clock.tick(60) / 1000.0  # Assuming 60 FPS as the desired frame rate

            self.textbox.container.rect.center = (150, 100)  # Adjust the position of the text box container
            self.textbox.container.update(delta_time)
            self.textbox.textbox.update(delta_time)
            text_surface = self.textbox.font.render(self.textbox.text, True, self.textbox.color)
            self.screen.blit(text_surface, self.textbox.position)

            


        
    def load_next_node(self):
        if self.out_of_bounds_check():
            
            next_level_id = get_node_id(self.level_id, self.exit_direction)
            if next_level_id != 0:
                self.level_id = next_level_id

                # Clear existing static bodies except for the character's body
                for body in self.world.bodies:
                    if body != self.character_body:
                        self.world.DestroyBody(body)
                self.enemies.clear()  # Clear list of enemies
                self.enemies_body.clear() #Clear list of enemy body objects
                self.tile_bodies.clear()
                self.npcs.clear()
                self.npcs_body.clear()

                self.level_data = load_level_data(self.level_id)
                self.level_width = len(self.level_data[0]) * tile_size  # Calculate the level width based on the tile size
                self.level_height = len(self.level_data) * tile_size # Calculate the level height based on the tile size
                self.camera.level_width = self.level_width
                self.camera.level_height = self.level_height

                self.update_player_position(self.exit_direction)

                # Create static bodies for the blue tiles in the new level data
                for y, row in enumerate(self.level_data):
                    for x, tile in enumerate(row):
                        if tile == 1:
                            tile_body = self.world.CreateStaticBody(
                                position=(x * tile_size, y * tile_size),
                                shapes=b2PolygonShape(box=(tile_size / 2, tile_size / 2))
                            )
                            self.tile_bodies.append(tile_body)
                        elif tile == 7:  # Spawn enemy at tile with value 7
                            enemy = Enemy(x * tile_size, y * tile_size, 50, 50)
                            enemy_body = self.world.CreateDynamicBody(
                                position=(x * tile_size, y * tile_size),
                                shapes=b2PolygonShape(box=(enemy.width / 2, enemy.height / 2)),
                                linearDamping=0.5,
                                angularDamping=0.5
                            )
                            self.enemies.append(enemy)  # Add enemy to a list
                            self.enemies_body.append(enemy_body) #add enemy body to a list
                        elif tile == 10:
                            invisible_tile_body = self.world.CreateStaticBody(
                                position=(x * tile_size, y * tile_size),
                                shapes=b2PolygonShape(box=(tile_size / 2 , tile_size / 2))
                            )
                        elif tile == 11:
                            npc = NPC(x * tile_size, y * tile_size, 50, 50, ["Hello, there!", "How are you?", "Nice weather today!"])
                            npc_body = self.world.CreateStaticBody(
                                position=(x * tile_size, y * tile_size),
                                shapes=b2PolygonShape(box=(tile_size / 2 , tile_size / 2))
                            )
                            self.npcs.append(npc)
                            self.npcs_body.append(npc_body)
