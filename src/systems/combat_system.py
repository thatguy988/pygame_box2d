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


    def check_if_all_enemies_dead(self):
        alive_enemies = [enemy for enemy in self.enemies if enemy.alive]
        if (alive_enemies == []):
            print("Battle Successful")
            
            self.game_over = True
    
    
    def perform_action(self, attack_or_magic_option, entity_selected, character_taking_action):
        if attack_or_magic_option == 'Attack':
            return self.perform_attack(entity_selected,character_taking_action)
        elif attack_or_magic_option in ['Fire', 'Water', 'Lightning', 'Earth']:
            self.magic_points_reduce(attack_or_magic_option, character_taking_action)
            return self.perform_magic(attack_or_magic_option, entity_selected)
        elif attack_or_magic_option == 'Flee':
            result = self.perform_flee()
            if result:
                return attack_or_magic_option
            else:
                print("Flee Failed lose a turn")
                return result
        else:
            return "Invalid action"

    def perform_attack(self, entity_selected,character):
            critical_success = random.random() < 0.3  # 30% chance of success
            if critical_success:
                self.num_turns_player -= 0.5
                entity_selected.health -= character.attack_power
                return "Successful critical attack (0.5 turn)"
            else:
                self.num_turns_player -= 1
                entity_selected.health -= character.attack_power
                return "Successful attack (1 turn)"

    def perform_magic(self, attack_or_magic_option,entity_selected):
        # Check if the magic matches the weakness of the entity_selected
        if entity_selected.weakness == attack_or_magic_option:
            self.num_turns_player -= 0.5
            entity_selected.health -= 20
            return "Successful magic attack (0.5 turn)"
        else:
            self.num_turns_player -= 1
            entity_selected.health -= 10
            return "Successful magic attack (1 turn)"
        
    def perform_flee(self):
        flee_success = random.random() < 0.5  # 50% chance of success
        return flee_success
        

    def magic_points_reduce(self, magic_option, character_performing_action):
        if magic_option in ['Fire','Water','Lightning','Earth']:
            character_performing_action.magic_points -= 10
    

    def enemy_perform_action(self, attack_or_magic_option, entity_selected, enemy_taking_action):
        if attack_or_magic_option == 'Attack':
            return self.enemy_perform_attack(entity_selected)
        elif attack_or_magic_option in ['Fire', 'Water', 'Lightning', 'Earth']:
            self.magic_points_reduce(attack_or_magic_option, enemy_taking_action)
            return self.enemy_perform_magic(attack_or_magic_option, entity_selected)
        else:
            return "Invalid action"

    def enemy_perform_attack(self, entity_selected):
            critical_success = random.random() < 0.3  # 30% chance of success
            if critical_success:
                self.num_turns_enemies -= 0.5
                entity_selected.health -= 20
                return "Successful critical attack (0.5 turn)"
            else:
                self.num_turns_enemies -= 1
                entity_selected.health -= 10
                return "Successful attack (1 turn)"

    def enemy_perform_magic(self, attack_or_magic_option,entity_selected):
        # Check if the magic matches the weakness of the entity_selected
        if entity_selected.weakness == attack_or_magic_option:
            self.num_turns_enemies -= 0.5
            entity_selected.health -= 10
            return "Successful magic attack (0.5 turn)"
        else:
            self.num_turns_enemies -= 1
            entity_selected.health -= 10
            return "Successful magic attack (1 turn)"
    
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
    
