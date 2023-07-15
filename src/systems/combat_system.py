import random

class CombatSystem:
    def __init__(self, enemies, characters,combat_ui,result,damage,attack_or_magic):
        self.enemies = enemies
        self.alive_characters = characters
        self.starting_player_characters = characters
        self.dead_characters = []
        self.enemies_turn = False
        self.players_turn = True
        self.num_turns_enemies = None
        self.num_turns_player = self.calculate_num_turns(self.alive_characters)
        self.player_index = 0
        self.enemy_index = 0
        self.game_over = False
        self.battle_successful = False
        self.combat_ui = combat_ui
        self.result = result
        self.damage = damage
        self.attack_or_magic_option = attack_or_magic

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
        alive_characters = [character for character in self.alive_characters if character.alive]
        if (alive_characters == []):
            self.game_over = True
    
    def update_enemy_list(self):
        alive_enemies = [enemy for enemy in self.enemies if enemy.alive]
        self.enemies = alive_enemies

    def update_character_lists(self):
        alive_characters = [character for character in self.alive_characters if character.alive]
        killed_characters = [character for character in self.alive_characters if not character.alive]
        revived_characters = [character for character in self.dead_characters if character.alive]
        dead_characters = [character for character in self.dead_characters if not character.alive]

        self.alive_characters = alive_characters + revived_characters
        self.dead_characters = killed_characters + dead_characters

    def perform_action(self, action_selected, target_entity, attacking_character):
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
            'Revive': self.perform_magic,
            'Flee': self.perform_flee,
            'Skip': self.perform_skip,
            'Scan': self.perform_scan
        }

        action_method = action_mapping.get(action_selected)
        if action_method:
            if action_selected in ['Fire', 'Water', 'Lightning', 'Earth', 'Healing','Revive']:
                if self.magic_points_check(action_selected, attacking_character):
                    self.magic_points_reduce(action_selected, attacking_character)
                    return action_method(action_selected,target_entity,attacking_character)
                else:
                    return "0 turn", 0, action_selected
            elif action_selected in ['Flee','Skip']:
                return action_method()
            elif action_selected in ['Scan']:
                return action_method(target_entity)
            return action_method(target_entity, attacking_character)
        else:
            return None, None, None

    def perform_scan(self,target_entity):
        return "0 turn", target_entity, "Scan"
    
        
    def perform_skip(self):
        return "0 turn", None, "Skip"

    def perform_attack(self, target_entity, attacking_character):
        # Perform an attack action with a chance of critical success
        # target_entity: The entity being attacked
        # attacking_character: The character initiating the attack

        critical_success_chance = 0.3  # 30% chance of success

        critical_success = random.random() < critical_success_chance

        if critical_success:
            damage = attacking_character.attack_power * 2
            target_entity.health -= damage
            return "0.5 turn", damage, "Critical"
        else:
            damage = attacking_character.attack_power
            target_entity.health -= damage
            return "1 turn", damage, "Attack"


            

    def perform_magic(self, magic_selected, target_entity, attacking_character):
        magic_effects = {
            'Fire': {'weakness': 'Fire', 'weakness_turns': 0.5, 'weakness_damage': 20,
                     'strength': 'Lightning', 'strength_turns': 1.0, 'strength_damage': 5},

            'Water': {'weakness': 'Water', 'weakness_turns': 0.5, 'weakness_damage': 20,
                      'strength': 'Lightning', 'strength_turns': 1.0, 'strength_damage': 5},
            
            'Lightning': {'weakness': 'Lightning', 'weakness_turns': 0.5, 'weakness_damage': 20, 
                          'strength': 'Lightning', 'strength_turns': 1.0, 'strength_damage': 5},

            'Earth': {'weakness': 'Earth', 'weakness_turns': 0.5, 'weakness_damage': 20,
                      'strength': 'Earth', 'strength_turns': 1.0, 'strength_damage': 5},

            'Healing': {'healing_power': 5, 'healing_damage': 5},

            'Revive':{'revive_power': 5}
        }

        if magic_selected in magic_effects:
            magic_effect = magic_effects[magic_selected]

            if 'weakness' in magic_effect and target_entity.weakness == magic_selected:
                target_entity.health -= magic_effect['weakness_damage']
                return "0.5 turn", magic_effect['weakness_damage'], magic_selected

            if 'strength' in magic_effect and target_entity.strength == magic_selected:
                target_entity.health -= magic_effect['strength_damage']
                return "1 turn", magic_effect['strength_damage'], magic_selected
            

            if 'healing_power' in magic_effect:
                prev_health = target_entity.health
                target_entity.health += magic_effect['healing_power'] * attacking_character.healing_power

                if target_entity.health > target_entity.max_health:
                    overflow_health = target_entity.health - target_entity.max_health
                    recovered_health = magic_effect['healing_power'] * attacking_character.healing_power - overflow_health
                    target_entity.health = target_entity.max_health
                    if recovered_health == 0:
                        attacking_character.magic_points += 20
                        return "0 turn", 0, magic_selected
                    return "1 turn", recovered_health, magic_selected

                recovered_health = target_entity.health - prev_health
                return "1 turn", recovered_health, magic_selected
            
            if 'revive_power' in magic_effect:
                target_entity.alive = True
                target_entity.health = (target_entity.max_health / 2)
                return "1 turn", target_entity.name, magic_selected

        # Magic attack is not a weakness or strength
        target_entity.health -= 10
        return "1 turn", 10
        
    def perform_flee(self):
        flee_chance = 0.5  # 50% chance of success
        flee_successful = random.random() < flee_chance
        if flee_successful:
            return "0 turn", None, "Flee"
        return "1 turn", None, flee_successful
    

    def magic_points_check(self, magic_option, character_performing_action):
        if magic_option in ['Fire','Water','Lightning','Earth']:
            if (character_performing_action.magic_points < 10):    
                return False
            else:
                return True
        elif magic_option in ['Healing','Revive']:
            if (character_performing_action.magic_points < 20):
                return False
            else:
                return True

    def magic_points_reduce(self, magic_option, character_performing_action):

        if magic_option in ['Fire','Water','Lightning','Earth']:
            character_performing_action.magic_points -= 10
        elif magic_option in ['Healing','Revive']:
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
                return "0.5 turn"
            else:
                self.num_turns_enemies -= 1
                entity_selected.health -= 10
                return "1 turn"

    def enemy_perform_magic(self, attack_or_magic_option,entity_selected):
        # Check if the magic matches the weakness of the entity_selected
        if entity_selected.weakness == attack_or_magic_option:
            self.num_turns_enemies -= 0.5
            entity_selected.health -= 20
            return "0.5 turn"
        elif entity_selected.strength == attack_or_magic_option:
            self.num_turns_enemies -= 1
            entity_selected.health -= 5
            return "1 turn"
        else:
            self.num_turns_enemies -= 1
            entity_selected.health -= 10
            return "1 turn"
    
    def handle_enemy_input(self):
        alive_characters = [character for character in self.alive_characters if character.alive]
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
    

    def handle_turns(self):
        self.check_if_all_enemies_dead()
        self.check_if_all_player_characters_dead()
        if self.battle_successful:
            [character.restore_health_and_magic() for character in self.starting_player_characters]
            return 3, True
        if self.game_over:
            return 1, True
        if(self.players_turn):
            if(self.check_if_players_turn()):
                character_taking_action = self.starting_player_characters[self.player_index]
                while(not character_taking_action.alive):
                    self.player_index += 1
                    if(self.player_index == len(self.starting_player_characters)):
                        self.player_index = 0
                    character_taking_action = self.starting_player_characters[self.player_index]

                action_selected, entity_selected=self.combat_ui.handle_input()  # Call handle_input method of CombatMenus
                if entity_selected != None:
                    self.result , self.damage, self.attack_or_magic_option= self.perform_action(action_selected, entity_selected,character_taking_action)
                    
                    if self.result == 'Flee':
                        return 3, True
                    
                    if self.damage != None:
                        if self.result == 'Revived':
                            self.update_character_lists()
                            self.combat_ui.update_character_options(self.alive_characters)
                            self.combat_ui.update_dead_character_options(self.dead_characters)  
                        else:
                            Alive = self.check_if_alive(entity_selected)
                            if Alive == False:
                                self.update_enemy_list()
                                self.combat_ui.update_enemy_options(self.enemies)
                            
                    self.increase_player_index(self.result) 
                    self.decrease_turn_counter(self.result)
                    
               
            else:
                self.num_turns_enemies = self.calculate_num_turns(self.enemies)
                self.players_turn = False
                self.enemy_index = 0
        else:
            if(self.check_if_enemies_turn()):
                enemy_taking_action = self.enemies[self.enemy_index]
                while(not enemy_taking_action.alive):
                    self.enemy_index += 1
                    if(self.enemy_index == len(self.enemies)):
                        self.player_index = 0
                    enemy_taking_action = self.enemies[self.enemy_index]

                attack_or_magic_option, entity_selected=self.handle_enemy_input()
                self.enemy_perform_action(attack_or_magic_option,entity_selected, enemy_taking_action)
                Alive = self.check_if_alive(entity_selected)
                if Alive == False:
                    self.update_character_lists()
                    self.combat_ui.update_character_options(self.alive_characters)
                    self.combat_ui.update_dead_character_options(self.dead_characters)
                    
                
                self.enemy_index += 1
                if(self.enemy_index == len(self.enemies)):
                    self.enemy_index = 0
            else:
                self.num_turns_player = self.calculate_num_turns(self.alive_characters)
                self.players_turn = True
                self.player_index = 0
        if(self.game_over == True):
            return 3, True
        return self.result, self.damage, self.attack_or_magic_option
    


    def increase_player_index(self,result):
        if result != '0 turn':
            self.player_index += 1
            if(self.player_index == len(self.starting_player_characters)):
                self.player_index = 0
        

    def decrease_turn_counter(self,result):
        if result == '0 turn':
            pass
        elif result == '0.5 turn':
            self.num_turns_player -= 0.5
        elif result == '1 turn':
            self.num_turns_player -= 1
