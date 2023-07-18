import random
from pygame.locals import *
import Box2D


class MovementSystem:

    def player_movement(self, keys, character_body, is_jumping):
         # Handle character movement
        if keys[K_SPACE] and not is_jumping:  # Check if not already jumping
            character_body.ApplyForceToCenter((0, -5000), wake=True)
            is_jumping = True  # Set jump state to True
        if keys[K_a]:
            character_body.ApplyForceToCenter((-30, 0), wake=True)
        if keys[K_d]:
            character_body.ApplyForceToCenter((30, 0), wake=True)
        return is_jumping
    
    def enemy_movement(self, enemies, enemies_body, direction_timer, direction_change_interval, time_step):
        for enemy, enemy_body in zip(enemies, enemies_body):
                enemy.move(enemy_body)
                # Apply a force to the enemy body
                if direction_timer <= 0.0:
                    # Generate a new random force for x-direction
                    force_y = random.uniform(-5000, -5000)
                    enemy_body.ApplyForceToCenter((0, 0), wake=True)
                    direction_timer = direction_change_interval
                else:
                    direction_timer -= time_step

    
    

    def kinematic_body_movement(self, platform_render, kinematic_bodies):
        tile_parameters = {
            49: {
                    'min_x_switch_distance': 0,
                    'max_x_switch_distance': 1000,
                    'min_y_switch_distance': 300,
                    'max_y_switch_distance': 0,
                    
                    'velocity_x': 0,
                    'velocity_y': -5,
                },

                50: {
                    'min_x_switch_distance': 500,
                    'max_x_switch_distance': 800,
                    'min_y_switch_distance': 1000,
                    'max_y_switch_distance': 0,
                    
                    'velocity_x': -5,
                    'velocity_y': 0,
                },
            }
        # Apply velocity to kinematic bodies
        for platform, body in zip(platform_render, kinematic_bodies):
            platform.move(body)

            # Get the current position of the platform
            x, y = platform.get_position()


            # Get the tile type of the platform
            tile_type = platform.get_tile_type()

            # Check if the tile type has parameters defined
            if tile_type in tile_parameters:
                params = tile_parameters[tile_type]
                min_x_switch_distance = params['min_x_switch_distance']
                max_x_switch_distance = params['max_x_switch_distance']
                min_y_switch_distance = params['min_y_switch_distance']
                max_y_switch_distance = params['max_y_switch_distance']
                tile_velocity_x = params['velocity_x']
                tile_velocity_y = params['velocity_y']

                # Check if the platform has reached the switch distance
                if x <= min_x_switch_distance:
                    body.linearVelocity = Box2D.b2Vec2(-tile_velocity_x, tile_velocity_y)
                elif x >= max_x_switch_distance:
                    body.linearVelocity = Box2D.b2Vec2(tile_velocity_x, tile_velocity_y)
                elif y >= min_y_switch_distance:
                    body.linearVelocity = Box2D.b2Vec2(tile_velocity_x, tile_velocity_y)
                elif y <= max_y_switch_distance:
                    body.linearVelocity = Box2D.b2Vec2(tile_velocity_x, -tile_velocity_y)
       




    # def kinematic_body_movement(self, platform_render, kinematic_bodies, velocity_x, velocity_y,min_switch_distance,max_switch_distance):
    #     # Apply velocity to kinematic bodies
    #     for platform, body in zip(platform_render,kinematic_bodies):
    #         platform.move(body)
    #         # Get the current position of the platform
    #         x, y = platform.get_position()

    #         # Check if the platform has reached the switch distance
    #         if x <= min_switch_distance:
    #             body.linearVelocity = Box2D.b2Vec2(-velocity_x, velocity_y)
    #         elif x >= max_switch_distance:
    #             body.linearVelocity = Box2D.b2Vec2(velocity_x, velocity_y)
