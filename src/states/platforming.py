import pygame
from pygame.locals import *
from Box2D import *
from entities.character import Character
from leveldata import load_level_data, get_node_id

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
tile_size = 64

class PlatformingState:
    def __init__(self, screen, level_id):
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

        if keys[K_SPACE]:
            self.character_body.ApplyForceToCenter((0, -100), wake=True)
        if keys[K_a]:
            self.character_body.ApplyForceToCenter((-100, 0), wake=True)
        if keys[K_d]:
            self.character_body.ApplyForceToCenter((100, 0), wake=True)

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
            self.exit_direction = "top"
            return True
        elif self.character.y > self.level_height:
            self.exit_direction = "bottom"
            return True

    def update(self):
        time_step = 1.0 / 60.0  # Update time step (60 FPS)
        velocity_iterations = 6  # Velocity iterations for physics solver
        position_iterations = 2  # Position iterations for physics solver
        self.world.Step(time_step, velocity_iterations, position_iterations)

        # Update the character's position based on the Box2D body
        self.character.x = self.character_body.position.x
        self.character.y = self.character_body.position.y

        if self.out_of_bounds_check():
            
            next_level_id = get_node_id(self.level_id, self.exit_direction)
            self.level_id = next_level_id

            # Clear existing static bodies except for the character's body
            for body in self.world.bodies:
                if body != self.character_body:
                    self.world.DestroyBody(body)


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

        # Draw the character relative to the camera position
        character_rect = pygame.Rect(
            self.character.x - self.camera.x,
            self.character.y - self.camera.y,
            self.character.width,
            self.character.height
        )
        
        pygame.draw.rect(self.screen, WHITE, character_rect)
