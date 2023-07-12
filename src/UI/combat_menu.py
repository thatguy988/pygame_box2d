
import pygame
import pygame_gui

class CombatMenus:
    def __init__(self, screen, player_characters,enemies):
        self.screen = screen
        self.manager = pygame_gui.UIManager(screen.get_size())

        # Options
        self.options = ['Attack', 'Magic', 'Flee']
        self.current_option_index = 0

        # Magic Options
        self.magic_options = ['Fire', 'Water', 'Lightning', 'Earth', 'Healing']
        self.current_magic_option_index = 0
        self.cursor_symbol = ">"

        # Key Pressed State
        self.key_pressed = False
        self.show_magic = False

        self.show_enemy_boxes = False

        self.current_enemy_option_index = 0
        self.enemy_options = []
        self.selected_action_option = None
        self.selected_enemy_option = None
        self.selected_magic = False

        # UITextBoxes
        self.menu_option_boxes = []
        self.magic_option_boxes = []

        self.enemy_option_boxes = []

        self.character_names = []
        self.character_healths = []
        self.character_magic_points = []

        for i, option in enumerate(self.options):
            cursor = self.cursor_symbol if i == self.current_option_index else " "
            text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((100, 350 + i * 30), (200, 30)),
                manager=self.manager,
                html_text=f"{cursor} {option}"
            )
            self.menu_option_boxes.append(text)

        for i, magic_option in enumerate(self.magic_options):
            cursor = self.cursor_symbol if i == self.current_magic_option_index else " "
            magic_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((300, 350 + i * 30), (200, 30)),
                manager=self.manager,
                html_text=f"{cursor} {magic_option}"
            )
            self.magic_option_boxes.append(magic_text)
            magic_text.hide()

        for i, character in enumerate(player_characters):
            character_name_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((i * 150, screen.get_height() - 70), (200, 30)),
                manager=self.manager,
                html_text=f"Health: {character.name}"
            )
            self.character_names.append(character_name_text)
            character_health_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((i * 150, screen.get_height() - 50), (200, 30)),
                manager=self.manager,
                html_text=f"Health: {character.health}"
            )
            self.character_healths.append(character_health_text)
            character_magic_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((i * 150, screen.get_height() - 30), (200, 30)),
                manager=self.manager,
                html_text=f"Magic: {character.magic_points}"
            )
            self.character_magic_points.append(character_magic_text)

        for i, enemy in enumerate(enemies):
            cursor = self.cursor_symbol if i == 0 else " "
            enemy_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((500, 350 + i * 30), (200, 30)),
                manager=self.manager,
                html_text=f"{cursor} Enemy {enemy.id_number}"
            )
            self.enemy_options.append(enemy) #put enemy objects in list
            self.enemy_option_boxes.append(enemy_text)
            enemy_text.hide()

        self.turn_counter_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((screen.get_width()/3.5, 10), (200, 30)),
            manager=self.manager,
            html_text=f"Turn: {len(player_characters)}"
        )
        self.characters_turn = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((screen.get_width()/40, 10), (200, 30)),
            manager=self.manager,
            html_text=f"Whose Turn: {player_characters[0].name}"
        )

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if self.selected_action_option and self.selected_enemy_option:
            self.selected_action_option = None
            self.selected_enemy_option = None
            
        if not self.key_pressed:
            if not self.show_enemy_boxes:
                if not self.show_magic:
                    self.handle_menu_navigation(keys)
                    selected_option = self.handle_menu_selection(keys)
                    if selected_option == 'Attack':
                        self.selected_action_option = selected_option
                        self.show_enemy_options()
                    elif selected_option == 'Flee':
                        self.selected_action_option = selected_option
                        return self.selected_action_option , 1
                    elif selected_option == 'Magic':
                        self.selected_magic = True
                        self.show_magic_menu()
                else:
                    self.handle_magic_navigation(keys)
                    selected_option = self.handle_magic_selection(keys)
                    if selected_option == 'Healing':
                        pass
                        #self.selected_action_option = selected_option
                        #self.show_player_side()
                    elif selected_option in ['Fire', 'Water', 'Lightning', 'Earth']:
                        self.selected_action_option = selected_option
                        self.show_enemy_options()
                    elif keys[pygame.K_a]:
                        self.key_pressed = True
                        self.remove_magic_menu()
            else:
                self.handle_enemy_navigation(keys)
                selected_option=self.handle_enemy_selection(keys)
                if selected_option:
                    self.selected_enemy_option = selected_option
                    self.remove_enemy_options()
                    if self.selected_magic:
                        self.remove_magic_menu()
                        self.selected_magic = not self.selected_magic
                    return self.selected_action_option, self.selected_enemy_option
                elif keys[pygame.K_a]:
                    self.key_pressed = True
                    self.remove_enemy_options()

        else:
            if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_SPACE] or keys[pygame.K_a]):
                self.key_pressed = False
        
        return self.selected_action_option, self.selected_enemy_option  # Default return values when no option is selected

    def handle_menu_navigation(self, keys):
        if keys[pygame.K_w]:
            self.current_option_index = (self.current_option_index - 1) % len(self.options)
            self.key_pressed = True
        elif keys[pygame.K_s]:
            self.current_option_index = (self.current_option_index + 1) % len(self.options)
            self.key_pressed = True

    def handle_menu_selection(self, keys):
        if keys[pygame.K_SPACE]:
            selected_option = self.options[self.current_option_index]
            self.key_pressed = True
            return selected_option

    def handle_magic_navigation(self, keys):
        if keys[pygame.K_w]:
            self.current_magic_option_index = (self.current_magic_option_index - 1) % len(self.magic_options)
            self.key_pressed = True
        elif keys[pygame.K_s]:
            self.current_magic_option_index = (self.current_magic_option_index + 1) % len(self.magic_options)
            self.key_pressed = True

    def handle_magic_selection(self, keys):
        if keys[pygame.K_SPACE]:
            selected_option = self.magic_options[self.current_magic_option_index]
            self.key_pressed = True
            return selected_option
        
    def handle_enemy_navigation(self,keys):
            if keys[pygame.K_w]:
                self.current_enemy_option_index = (self.current_enemy_option_index - 1) % len(self.enemy_options)
                self.key_pressed = True
            elif keys[pygame.K_s]:
                self.current_enemy_option_index = (self.current_enemy_option_index + 1) % len(self.enemy_options)
                self.key_pressed = True
        
        


    def handle_enemy_selection(self, keys):
        if keys[pygame.K_SPACE]:
            selected_option = self.enemy_options[self.current_enemy_option_index]
            self.key_pressed = True
            return selected_option #return enemy object
        
    
    def show_enemy_options(self):
        self.current_enemy_option_index = 0
        self.show_enemy_boxes = not self.show_enemy_boxes
        for attack_text in self.enemy_option_boxes:
            attack_text.show()

    def remove_enemy_options(self):
        self.show_enemy_boxes = not self.show_enemy_boxes
        for attack_text in self.enemy_option_boxes:
            attack_text.hide()

    def show_magic_menu(self):
        self.current_magic_option_index = 0
        self.show_magic = not self.show_magic
        for magic_text in self.magic_option_boxes:
            magic_text.show()

    def remove_magic_menu(self):
        self.show_magic = not self.show_magic
        for magic_text in self.magic_option_boxes:
            magic_text.hide()

    def enemy_dead(self, enemies):
        alive_enemies = [enemy for enemy in enemies if enemy.alive]
        self.enemy_option_boxes = []
        self.enemy_options = []
        for i, enemy in enumerate(alive_enemies):
            cursor = self.cursor_symbol if i == 0 else " "
            enemy_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((500, 350 + i * 30), (200, 30)),
                manager=self.manager,
                html_text=f"{cursor} Enemy {enemy.id_number}"
            )
            self.enemy_options.append(enemy)
            self.enemy_option_boxes.append(enemy_text)
            enemy_text.hide()
        


    

    def render(self,player_characters,enemies,num_of_player_turns,character_taking_action):

        # Render the menu options
        for i, option in enumerate(self.options):
            cursor = self.cursor_symbol if i == self.current_option_index else " "
            text = self.menu_option_boxes[i]
            text.set_text(f"{cursor} {option}")

        if self.show_magic:
            # Render the magic menu options
            for i, magic_option in enumerate(self.magic_options):
                cursor = self.cursor_symbol if i == self.current_magic_option_index else " "
                text = self.magic_option_boxes[i]
                text.set_text(f"{cursor} {magic_option}")

        # Render character names, health, and magic points
        for i, character in enumerate(player_characters):
            character_name_text = self.character_names[i]
            character_name_text.set_text(f"Name: {character.name}")

            character_health_text = self.character_healths[i]
            character_health_text.set_text(f"Health: {character.health}")

            character_magic_text = self.character_magic_points[i]
            character_magic_text.set_text(f"Magic: {character.magic_points}")

        if self.show_enemy_boxes:
            for i, enemy in enumerate(enemies):
                cursor = self.cursor_symbol if i == self.current_enemy_option_index else " "
                text = self.enemy_option_boxes[i]
                text.set_text(f"{cursor} Enemy {enemy.id_number}")

        self.turn_counter_text.set_text(f"Turn: {num_of_player_turns}")
        self.characters_turn.set_text(f"Whose Turn: {character_taking_action.name}" )

                

        
        self.manager.update(pygame.time.get_ticks() / 1000.0)
        self.manager.draw_ui(self.screen)




