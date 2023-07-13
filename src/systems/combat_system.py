import random

class CombatSystem:
    def __init__(self, enemies, characters):
        self.enemies = enemies
        self.characters = characters
        self.enemies_turn = False
        self.players_turn = True
        self.num_turns_enemies = None
        self.num_turns_player = self.calculate_num_turns(self.characters)
        self.player_index = 0
        self.enemy_index = 0
        self.game_over = False
        self.battle_successful = False

    def calculate_num_turns(self, entities):
        num_turns = sum(1 for entity in entities if entity.alive)
        return num_turns
    
    def check_if_players_turn(self):
        if(self.num_turns_player > 0):
            return True
        else:
            return False
        
    def check_if_enemies_turn(self):
        if(self.num_turns_enemies > 0):
            return True
        else:
            return False
        
    def check_if_alive(self,entity_selected):
        if(entity_selected.health <= 0):
            entity_selected.alive = False
            return False
        return True


    def check_if_all_enemies_dead(self):
        alive_enemies = [enemy for enemy in self.enemies if enemy.alive]
        if (alive_enemies == []):
            self.battle_successful = True

    def check_if_all_player_characters_dead(self):
        alive_characters = [character for character in self.characters if character.alive]
        if (alive_characters == []):
            self.game_over = True
    
    def reorganize(self):
        alive_enemies = [enemy for enemy in self.enemies if enemy.alive]
        self.enemies = alive_enemies

    def perform_action(self, attack_or_magic_option, target_entity, attacking_character):
        # Perform the specified action based on the given option
        # attack_or_magic_option: The selected action option
        # target_entity: The entity on which the action is performed
        # attacking_character: The character initiating the action

        action_mapping = {
            'Attack': self.perform_attack,
            'Fire': self.perform_magic,
            'Water': self.perform_magic,
            'Lightning': self.perform_magic,
            'Earth': self.perform_magic,
            'Healing': self.perform_magic,
            'Flee': self.perform_flee,
            'Skip': self.perform_skip
        }

        action_method = action_mapping.get(attack_or_magic_option)
        if action_method:
            if attack_or_magic_option in ['Fire', 'Water', 'Lightning', 'Earth', 'Healing']:
                self.magic_points_reduce(attack_or_magic_option, attacking_character)
                return action_method(attack_or_magic_option,target_entity,attacking_character)
            elif attack_or_magic_option in ['Flee','Skip']:
                return action_method(), None
            return action_method(target_entity, attacking_character)
        else:
            return None, None

    
    
        
    def perform_skip(self):
        self.num_turns_player -= 0.5
        return "Skip"

    def perform_attack(self, target_entity, attacking_character):
        # Perform an attack action with a chance of critical success
        # target_entity: The entity being attacked
        # attacking_character: The character initiating the attack

        critical_success_chance = 0.3  # 30% chance of success

        critical_success = random.random() < critical_success_chance

        if critical_success:
            self.num_turns_player -= 0.5
            damage = attacking_character.attack_power * 2
            target_entity.health -= damage
            return "Critical (0.5 turn)", damage
        else:
            self.num_turns_player -= 1
            damage = attacking_character.attack_power
            target_entity.health -= damage
            return "Attack (1 turn)", damage


            

    def perform_magic(self, attack_or_magic_option, target_entity, attacking_character):
        magic_effects = {
            'Fire': {'weakness': 'Fire', 'weakness_turns': 0.5, 'weakness_damage': 20,
                     'strength': 'Lightning', 'strength_turns': 1.0, 'strength_damage': 5},

            'Water': {'weakness': 'Water', 'weakness_turns': 0.5, 'weakness_damage': 20,
                      'strength': 'Lightning', 'strength_turns': 1.0, 'strength_damage': 5},
            
            'Lightning': {'weakness': 'Lightning', 'weakness_turns': 0.5, 'weakness_damage': 20, 
                          'strength': 'Lightning', 'strength_turns': 1.0, 'strength_damage': 5},

            'Earth': {'weakness': 'Earth', 'weakness_turns': 0.5, 'weakness_damage': 20,
                      'strength': 'Earth', 'strength_turns': 1.0, 'strength_damage': 5},

            'Healing': {'healing_power': 5, 'healing_damage': 5}
        }

        if attack_or_magic_option in magic_effects:
            magic_effect = magic_effects[attack_or_magic_option]

            if 'weakness' in magic_effect and target_entity.weakness == attack_or_magic_option:
                self.num_turns_player -= magic_effect['weakness_turns']
                target_entity.health -= magic_effect['weakness_damage']
                return "Weak (0.5 turn)", magic_effect['weakness_damage']

            if 'strength' in magic_effect and target_entity.strength == attack_or_magic_option:
                self.num_turns_player -= magic_effect['strength_turns']
                target_entity.health -= magic_effect['strength_damage']
                return "Resist (1 turn)", magic_effect['strength_damage']
            

            if 'healing_power' in magic_effect:
                prev_health = target_entity.health
                target_entity.health += magic_effect['healing_power'] * attacking_character.healing_power

                if target_entity.health > target_entity.max_health:
                    overflow_health = target_entity.health - target_entity.max_health
                    recovered_health = magic_effect['healing_power'] * attacking_character.healing_power - overflow_health
                    target_entity.health = target_entity.max_health
                    if recovered_health == 0:
                        attacking_character.magic_points += 20
                        self.num_turns_player += 1
                        self.player_index -= 1
                    self.num_turns_player -= 1
                    return "Max Health Reached", recovered_health

                recovered_health = target_entity.health - prev_health
                self.num_turns_player -= 1
                return "Healing", recovered_health

        # Magic attack is not a weakness or strength
        self.num_turns_player -= 1
        target_entity.health -= 10
        return "Magic attack (1 turn)", 10


    # def perform_magic(self, attack_or_magic_option, entity_selected, character_taking_action):
    #     if attack_or_magic_option in ['Fire','Water','Lightning','Earth']:
    #         if entity_selected.weakness == attack_or_magic_option:
    #             self.num_turns_player -= 0.5
    #             entity_selected.health -= 20
    #             return "Weak (0.5 turn)", 20
    #         elif entity_selected.strength == attack_or_magic_option:
    #             self.num_turns_player -= 1 
    #             entity_selected.health -= 5
    #             return "Resist (1 turn)", 5
    #         else:
    #             self.num_turns_player -= 1
    #             entity_selected.health -= 10
    #             return "Magic attack (1 turn)", 10
    #     elif attack_or_magic_option in ['Healing']:

    #         prev_health = entity_selected.health
    #         entity_selected.health += 5 * character_taking_action.healing_power

    #         if entity_selected.health > entity_selected.max_health:
    #             overflow_health = entity_selected.health - entity_selected.max_health 
    #             recovered_health = (5 * character_taking_action.healing_power) - overflow_health
    #             entity_selected.health = entity_selected.max_health
    #             if(recovered_health == 0):
    #                 character_taking_action.magic_points += 20
    #                 self.num_turns_player += 1
    #                 self.player_index -= 1
    #             self.num_turns_player -= 1    
    #             return "Max Health Reached", recovered_health
    #         self.num_turns_player -= 1
    #         recovered_health = entity_selected.health - prev_health
    #         return "Healing", recovered_health
        
    def perform_flee(self):
        flee_chance = 0.5  # 50% chance of success
        flee_successful = random.random() < flee_chance
        self.num_turns_player -= 1
        if flee_successful:
            return "Flee"
        return flee_successful
    

        

    def magic_points_reduce(self, magic_option, character_performing_action):
        if magic_option in ['Fire','Water','Lightning','Earth']:
            character_performing_action.magic_points -= 10
        elif magic_option in ['Healing']:
            character_performing_action.magic_points -= 20
    

    def enemy_perform_action(self, attack_or_magic_option, entity_selected, enemy_taking_action):
        if attack_or_magic_option == 'Attack':
            return self.enemy_perform_attack(entity_selected)
        elif attack_or_magic_option in ['Fire', 'Water', 'Lightning', 'Earth']:
            self.magic_points_reduce(attack_or_magic_option, enemy_taking_action)
            return self.enemy_perform_magic(attack_or_magic_option, entity_selected)
        else:
            return None, None

    def enemy_perform_attack(self, entity_selected):
            critical_success = random.random() < 0.3  # 30% chance of success
            if critical_success:
                self.num_turns_enemies -= 0.5
                entity_selected.health -= 20
                return "Critical (0.5 turn)"
            else:
                self.num_turns_enemies -= 1
                entity_selected.health -= 10
                return "Attack (1 turn)"

    def enemy_perform_magic(self, attack_or_magic_option,entity_selected):
        # Check if the magic matches the weakness of the entity_selected
        if entity_selected.weakness == attack_or_magic_option:
            self.num_turns_enemies -= 0.5
            entity_selected.health -= 20
            return "Weak (0.5 turn)"
        elif entity_selected.strength == attack_or_magic_option:
            self.num_turns_enemies -= 1
            entity_selected.health -= 5
            return "Resist (1 turn)"
        else:
            self.num_turns_enemies -= 1
            entity_selected.health -= 10
            return "Magic attack (1 turn)"
    
    def handle_enemy_input(self):
        alive_characters = [character for character in self.characters if character.alive]
        if (alive_characters == []):
            self.game_over = True
            return None, None
        selected_action = random.choice(['Attack', 'Magic'])
        if selected_action == 'Attack':
            selected_target = random.choice(alive_characters)
        elif selected_action == 'Magic':
            selected_magic = random.choice(['Fire','Water','Lightning','Earth'])
            selected_target = random.choice(alive_characters)
            return selected_magic, selected_target

        return selected_action, selected_target
    
