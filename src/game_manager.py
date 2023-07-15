import pygame
import random

from pygame.locals import *
from Box2D import *


from entities.character import Character
from entities.enemy import Enemy 
from entities.npc import NPC
from leveldata.load_data import load_level_data, get_node_id
from systems.collision import CollisionSystem 
from systems.movement import MovementSystem
from systems.combat_system import CombatSystem
from camera import Camera
from UI.textbox import TextBox
from UI.combat_menu import CombatMenus
from pygame_gui import UIManager

tile_size = 64

class GameManager:
    def __init__(self):
        pass

    def initialize_platforming_state(self,screen,level_id,key_pressed):
        self.enemies = []
        self.enemies_physical_body = []
        self.tile_physical_bodies = []
        self.npcs = []
        self.npcs_physical_body = []
        self.screen = screen
        tile_size = 64  # Adjust the size of the tile as needed
        self.exit_direction = None  # Initialize exit direction variable
        self.level_id=level_id
        self.level_data = load_level_data(self.level_id)
        self.camera_speed = 0.25
        self.level_width = len(self.level_data[0]) * tile_size  # Calculate the level width based on the tile size
        self.level_height = len(self.level_data) * tile_size # Calculate the level height based on the tile size
        player_position = self.find_player_position()
        self.character = Character.create_character(player_position[0] * tile_size, player_position[1] * tile_size, "Player 1")
        self.companion_1 = Character.create_character(0, 0, "Player 2")
        self.companion_2 = Character.create_character(0, 0, "Player 3")
        self.companion_3 = Character.create_character(0, 0, "Player 4")
        
        self.is_jumping = False  # Variable to track jump state
        self.direction_change_interval = 20.0  # Time interval for changing direction (in seconds)
        self.direction_timer = 0.0  # Timer to keep track of time passed
        self.collision = CollisionSystem()
        self.movement = MovementSystem()
        self.ui_manager = UIManager((screen.get_width(), screen.get_height()))
        self.textbox = TextBox((50, 50), (200, 100), pygame.font.Font(None, 24), pygame.Color("white"), self.ui_manager)
        self.clock= pygame.time.Clock()

        self.npc_talk = False
        self.text_render = False
        self.key_pressed = key_pressed
        self.camera = Camera(self.screen, self.level_width, self.level_height, self.camera_speed)
        # Create a Box2D world
        self.world = b2World(gravity=(0, 10), doSleep=True)


        self.tile_physical_bodies = [
            self.world.CreateStaticBody(
                position=(x * tile_size, y * tile_size),
                shapes=b2PolygonShape(box=(tile_size / 2, tile_size / 2))
            )
            for y, row in enumerate(self.level_data)
            for x, tile in enumerate(row)
            if tile == 1
        ]

        self.enemies_physical_body = [
            (
                self.world.CreateDynamicBody(
                    position=(x * tile_size, y * tile_size),
                    shapes=b2PolygonShape(box=(enemy.width / 2, enemy.height / 2)),
                    linearDamping=0.5,
                    angularDamping=0.5
                ),
                self.enemies.append(enemy)
            )[0]  # Return the physical body to the list
            for y, row in enumerate(self.level_data)
            for x, tile in enumerate(row)
            if tile == 7
            for enemy in [Enemy.create_enemy(x * tile_size, y * tile_size, "slime")]
        ]


        self.tile_physical_bodies += [
            self.world.CreateStaticBody(
                position=(x * tile_size, y * tile_size),
                shapes=b2PolygonShape(box=(tile_size / 2, tile_size / 2))
            )
            for y, row in enumerate(self.level_data)
            for x, tile in enumerate(row)
            if tile == 10
        ]

        self.npcs_physical_body = [
            (
                self.world.CreateStaticBody(
                    position=(x * tile_size, y * tile_size),
                    shapes=b2PolygonShape(box=(tile_size / 2, tile_size / 2))
                ),
                self.npcs.append(npc)
            )[0]  # Return the physical body to the list
            for y, row in enumerate(self.level_data)
            for x, tile in enumerate(row)
            if tile == 11
            for npc in [NPC(x * tile_size, y * tile_size, 50, 50, ["Hello, there!", "How are you?", "Nice weather today!"])]
        ]
                    
        # Create a dynamic character body
        self.character_physical_body = self.world.CreateDynamicBody(
            position=(player_position[0]*tile_size, player_position[1]*tile_size),
            shapes=b2PolygonShape(box=(self.character.width / 2 , self.character.height / 2)),
            linearDamping=0.5,
            angularDamping=0.5
        )
    def find_player_position(self):
            for y, row in enumerate(self.level_data):
                for x, tile in enumerate(row):
                    if tile == 2:
                        return (x, y)
            return (0, 0)  # Default to (0, 0) if no player position is found  
    
    def is_character_out_of_bounds_check(self):
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
        
    def update_player_position(self, exit_direction):
        #switch tile to spawn at 3,4,5, or 6
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
            self.character_physical_body.position = b2Vec2(player_position[0] * tile_size, player_position[1] * tile_size)
    

    def load_next_node(self):
        if self.is_character_out_of_bounds_check():
            
            next_level_id = get_node_id(self.level_id, self.exit_direction)
            if next_level_id != 0:
                self.level_id = next_level_id

                # Clear existing static bodies except for the character's body
                for body in self.world.bodies:
                    if body != self.character_physical_body:
                        self.world.DestroyBody(body)
                self.enemies.clear()  # Clear list of enemies
                self.enemies_physical_body.clear() #Clear list of enemy body objects
                self.tile_physical_bodies.clear()
                self.npcs.clear()
                self.npcs_physical_body.clear()

                self.level_data = load_level_data(self.level_id)
                self.level_width = len(self.level_data[0]) * tile_size  # Calculate the level width based on the tile size
                self.level_height = len(self.level_data) * tile_size # Calculate the level height based on the tile size
                self.camera.level_width = self.level_width
                self.camera.level_height = self.level_height

                self.update_player_position(self.exit_direction)


                self.tile_physical_bodies = [
                    self.world.CreateStaticBody(
                        position=(x * tile_size, y * tile_size),
                        shapes=b2PolygonShape(box=(tile_size / 2, tile_size / 2))
                    )
                    for y, row in enumerate(self.level_data)
                    for x, tile in enumerate(row)
                    if tile == 1
                ]

                self.enemies_physical_body = [
                    (
                        self.world.CreateDynamicBody(
                            position=(x * tile_size, y * tile_size),
                            shapes=b2PolygonShape(box=(enemy.width / 2, enemy.height / 2)),
                            linearDamping=0.5,
                            angularDamping=0.5
                        ),
                        self.enemies.append(enemy)
                    )[0]  # Return the physical body to the list
                    for y, row in enumerate(self.level_data)
                    for x, tile in enumerate(row)
                    if tile == 7
                    for enemy in [Enemy.create_enemy(x * tile_size, y * tile_size, "slime")]
                ]


                self.tile_physical_bodies += [
                    self.world.CreateStaticBody(
                        position=(x * tile_size, y * tile_size),
                        shapes=b2PolygonShape(box=(tile_size / 2, tile_size / 2))
                    )
                    for y, row in enumerate(self.level_data)
                    for x, tile in enumerate(row)
                    if tile == 10
                ]

                self.npcs_physical_body = [
                    (
                        self.world.CreateStaticBody(
                            position=(x * tile_size, y * tile_size),
                            shapes=b2PolygonShape(box=(tile_size / 2, tile_size / 2))
                        ),
                        self.npcs.append(npc)
                    )[0]  # Return the physical body to the list
                    for y, row in enumerate(self.level_data)
                    for x, tile in enumerate(row)
                    if tile == 11
                    for npc in [NPC(x * tile_size, y * tile_size, 50, 50, ["Hello, there!", "How are you?", "Nice weather today!"])]
                ]

    def initialize_combat_state(self,screen,key_pressed,enemy):
        self.screen = screen
        self.key_pressed = key_pressed
        self.starting_player_characters = [
            self.character,
            self.companion_1,
            self.companion_2,
            self.companion_3
        ]
        self.result = None
        self.damage = None
        
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

            
            self.character.rect = pygame.Rect(player_x, player_y, player_width, player_height)
            self.companion_1.rect = pygame.Rect(player_x, player_y + 70, 50, 50)
            self.companion_2.rect = pygame.Rect(player_x, player_y + 140, 50, 50)
            self.companion_3.rect = pygame.Rect(player_x, player_y + 210, 50, 50)

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
                CombatMenus(screen, self.starting_player_characters, self.enemies,self.result,self.damage)
            
            self.combat_system = CombatSystem(self.enemies,self.starting_player_characters,self.combat_menus)


