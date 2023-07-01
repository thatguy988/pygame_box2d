import pygame
import random

from pygame.locals import *
from Box2D import *
from entities.character import Character
from entities.enemy import Enemy 
from leveldata import load_level_data, get_node_id

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
tile_size = 64

class PlatformingState:
    def __init__(self, screen, level_id):
        self.enemies = []
        self.enemies_body = []
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
        self.direction_change_interval = 10.0  # Time interval for changing direction (in seconds)
        self.direction_timer = 0.0  # Timer to keep track of time passed

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
        
        
        # Handle character movement
        if keys[K_SPACE] and not self.is_jumping:  # Check if not already jumping
            self.character_body.ApplyForceToCenter((0, -5000), wake=True)
            self.is_jumping = True  # Set jump state to True
        if keys[K_a]:
            self.character_body.ApplyForceToCenter((-50, 0), wake=True)
        if keys[K_d]:
            self.character_body.ApplyForceToCenter((50, 0), wake=True)

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

        # Update enemy positions based on the Box2D bodies
        for enemy, enemy_body in zip(self.enemies, self.enemies_body):
            # Update enemy positions based on the Box2D bodies
            for enemy, enemy_body in zip(self.enemies, self.enemies_body):
                enemy.move(enemy_body)
                # Apply a force to the enemy body
                if self.direction_timer <= 0.0:
                    # Generate a new random force for x-direction
                    force_x = random.uniform(-500, 500)
                    enemy_body.ApplyForceToCenter((force_x, 0), wake=True)
                    self.direction_timer = self.direction_change_interval
                else:
                    self.direction_timer -= time_step
                
                # Check for contact between enemy and character
                for contact_edge in self.character_body.contacts:
                    contact = contact_edge.contact
                    fixture_a = contact.fixtureA
                    fixture_b = contact.fixtureB
                    if fixture_a.body == enemy_body or fixture_b.body == enemy_body:
                        # Check if the character is on top of the enemy
                        character_bottom = self.character_body.position.y + self.character.height / 2
                        enemy_top = enemy_body.position.y - enemy.height / 2
                        top_hit = character_bottom < enemy_top  # Flag to track if a "Top hit" occurs

                        if top_hit:
                            print("Top hit")
                        else:
                            # Check if the character's left or right side makes contact with the enemy's left or right side
                            character_left = self.character_body.position.x - self.character.width / 2
                            character_right = self.character_body.position.x + self.character.width / 2
                            enemy_left = enemy_body.position.x - enemy.width / 2
                            enemy_right = enemy_body.position.x + enemy.width / 2

                            if character_right >= enemy_left and character_left <= enemy_left:
                                print("Left side hit")
                            elif character_left <= enemy_right and character_right >= enemy_right:
                                print("Right side hit")

        
                
        # Check if the character is on the ground
        if self.character_body.contacts:
            self.is_jumping = False  
        
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
