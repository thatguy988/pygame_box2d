import random
from pygame.locals import *


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
