import pygame
import random

from pygame.locals import *
from Box2D import *
from entities.character import Character
from entities.enemy import Enemy 
from entities.npc import NPC
from leveldata import load_level_data, get_node_id
from systems.collision import CollisionSystem 
from systems.movement import MovementSystem
from UI.textbox import TextBox

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
tile_size = 64

class PlatformingState:
    def __init__(self, screen, level_id):
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
        self.camera = pygame.math.Vector2(player_position[0] * tile_size, player_position[1] * tile_size)
        self.character = Character(player_position[0] * tile_size, player_position[1] * tile_size, 50, 50)
        self.is_jumping = False  # Variable to track jump state
        self.direction_change_interval = 20.0  # Time interval for changing direction (in seconds)
        self.direction_timer = 0.0  # Timer to keep track of time passed
        self.leftside = False
        self.rightside = False
        self.collision = CollisionSystem()
        self.movement = MovementSystem()
        self.textbox = TextBox((50, 50), (200, 100), pygame.font.Font(None, 24), pygame.Color("white"))
        self.npc_talk = False
        self.text_render = False
        self.key_pressed = False


        

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

        if keys[K_ESCAPE]:  
            return 1
        
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

        
        
        self.is_jumping = self.movement.apply_force(keys, self.character_body, self.is_jumping)
        
        
       

        return None  # No state transition
    
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
        self.collision.check_collision(self.enemies, self.enemies_body,self.character, self.character_body, self.world)
        self.npc_talk = self.collision.npc_collision(self.npcs, self.npcs_body, self.character, self.character_body,self.textbox)
        for enemy, enemy_body in zip(self.enemies, self.enemies_body):
                enemy.move(enemy_body)
                # Apply a force to the enemy body
                if self.direction_timer <= 0.0:
                    # Generate a new random force for x-direction
                    force_y = random.uniform(-5000, -5000)
                    enemy_body.ApplyForceToCenter((0, 0), wake=True)
                    self.direction_timer = self.direction_change_interval
                else:
                    self.direction_timer -= time_step
    
        # # Check if the character is on the ground
        # if self.character_body.contacts:
        #     self.is_jumping = False  
        # Check if the character is on the ground
        if self.character_body.contacts:
            character_bottom = self.character_body.position.y + self.character.height / 2

            for tile_body in self.tile_bodies:
                tile_top = tile_body.position.y - tile_size / 2

                if character_bottom > tile_top:
                    self.is_jumping = False
                    break

        self.next_node()

    def render(self):
        # Smoothly adjust the camera position to center the player
        camera_target = pygame.math.Vector2(
            self.character.x - self.screen.get_width() / 2,
            self.character.y - self.screen.get_height() / 2
        )
        self.camera += (camera_target - self.camera) * self.camera_speed
        self.camera.x = max(0, min(self.camera.x, self.level_width - self.screen.get_width()))
        self.camera.y = max(0, min(self.camera.y, self.level_height - self.screen.get_height()))


        self.screen.fill((0, 0, 0))  # Clear the screen

        for y, row in enumerate(self.level_data):
            for x, tile in enumerate(row):
                if tile == 1:
                    tile_rect = pygame.Rect(x * tile_size - self.camera.x, y * tile_size - self.camera.y, tile_size, tile_size)
                    pygame.draw.rect(self.screen, BLUE, tile_rect)
                elif tile == 11:
                    npc_rect = pygame.Rect(x * tile_size - self.camera.x, y * tile_size - self.camera.y, tile_size, tile_size)
                    pygame.draw.rect(self.screen, (255,165,255), npc_rect)
                
        # Render the enemies
        for enemy in self.enemies:
            enemy_rect = pygame.Rect(
                enemy.x - self.camera.x,
                enemy.y - self.camera.y,
                enemy.width,
                enemy.height
            )
            pygame.draw.rect(self.screen, (255,165,0), enemy_rect)

        # Draw the character relative to the camera position
        character_rect = pygame.Rect(
            self.character.x - self.camera.x,
            self.character.y - self.camera.y,
            self.character.width,
            self.character.height
        )
        
        pygame.draw.rect(self.screen, WHITE, character_rect)
        if self.text_render:
            print("i am here")
            self.textbox.render(self.screen)



    def next_node(self):
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

                self.level_data = load_level_data(self.level_id)

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
