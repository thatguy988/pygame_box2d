import random
class CollisionSystem:
    def __init__(self):
        # Initialize collision system
        pass

    def check_collision(self, enemies, enemies_body,character, character_body, world):
        # Update enemy positions based on the Box2D bodies
        for enemy, enemy_body in zip(enemies, enemies_body):
                # Check for contact between enemy and character
                for contact_edge in character_body.contacts:
                    contact = contact_edge.contact
                    fixture_a = contact.fixtureA
                    fixture_b = contact.fixtureB
                    if fixture_a.body == enemy_body or fixture_b.body == enemy_body:
                        # Check if the character is on top of the enemy
                        character_bottom = character_body.position.y + character.height / 2
                        enemy_top = enemy_body.position.y - enemy.height / 2
                        top_hit = character_bottom < enemy_top  # Flag to track if a "Top hit" occurs

                        if top_hit:
                            print("Top hit")
                            enemies.remove(enemy) #remove enemy
                            world.DestroyBody(enemy_body) #remove object from world
                            enemies_body.remove(enemy_body)  #remove  objec from list 
                        else:
                            # Check if the character's left or right side makes contact with the enemy's left or right side
                            character_left = character_body.position.x - character.width / 2
                            character_right = character_body.position.x + character.width / 2
                            enemy_left = enemy_body.position.x - enemy.width / 2
                            enemy_right = enemy_body.position.x + enemy.width / 2

                            if character_right >= enemy_left and character_left <= enemy_left:
                                print("bottom hit") # originally left side hit
                            elif character_left <= enemy_right and character_right >= enemy_right:
                                print("bottom hit") # originally right side hit
                            else:
                                # Check if the bottom of the enemy makes contact with the side of the character
                                enemy_bottom = enemy_body.position.y + enemy.height / 2
                                character_top = character_body.position.y - character.height / 2
                                bottom_hit = enemy_bottom > character_top  # Flag to track if a "side hit" occurs

                                if bottom_hit:
                                    print("side hit") # originally bottom hit
    
        # # Check if the character is on the ground
        # if self.character_body.contacts:
        #     self.is_jumping = False  
        # Check if the character is on the ground
        # if self.character_body.contacts:
        #     character_bottom = self.character_body.position.y + self.character.height / 2

        #     for tile_body in self.tile_bodies:
        #         tile_top = tile_body.position.y - tile_size / 2

        #         if character_bottom > tile_top:
        #             self.is_jumping = False
        #             break

    def handle_collision(self, entity1, entity2):
        # Handle collision between entity1 and entity2
        pass
    def npc_collision(self, npcs, npcs_body, character, character_body,textbox):
        # Check if the bottom of the enemy makes contact with the side of the character
        for npc, npc_body in zip(npcs, npcs_body):
            for contact_edge in character_body.contacts:
                    contact = contact_edge.contact
                    fixture_a = contact.fixtureA
                    fixture_b = contact.fixtureB
                    if fixture_a.body == npc_body or fixture_b.body == npc_body:
                        npc_bottom = npc_body.position.y + npc.height / 2
                        character_top = character_body.position.y - character.height / 2
                        side_hit = npc_bottom > character_top  # Flag to track if a "side hit" occurs

                        if side_hit:
                            textbox.set_text(npc.dialogue[0])

                            #print(" npc side hit") # originally bottom hit
                            return side_hit

# Other functions and classes related to collision
