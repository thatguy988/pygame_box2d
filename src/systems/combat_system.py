import random

class CombatSystem:
    def __init__(self, enemies, characters):
        self.enemies = enemies
        self.characters = characters
        self.num_turns_enemies = self.calculate_num_turns(self.enemies)
        self.num_turns_player = self.calculate_num_turns(self.characters)

    def calculate_num_turns(self, entities):
        num_turns = sum(1 for entity in entities if entity.alive)
        return num_turns

    def perform_action(self, attack_or_magic_option, entity_selected):
        if attack_or_magic_option == 'Attack':
            return self.perform_attack(entity_selected)
        elif attack_or_magic_option in ['Fire', 'Water', 'Lightning', 'Earth']:
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

    def perform_attack(self, entity_selected):
            critical_success = random.random() < 0.3  # 30% chance of success
            if critical_success:
                return "Successful critical attack (0.5 turn)"
            else:
                return "Successful attack (1 turn)"

    def perform_magic(self, attack_or_magic_option,entity_selected):
        # Check if the magic matches the weakness of the entity_selected
        if entity_selected.weakness == attack_or_magic_option:
            return "Successful magic attack (0.5 turn)"
        else:
            return "Successful magic attack (1 turn)"
        
    def perform_flee(self):
        flee_success = random.random() < 0.5  # 50% chance of success
        return flee_success
