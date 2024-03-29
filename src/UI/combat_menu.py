import pygame
import pygame_gui


class CombatMenus:
    def __init__(self, screen, player_characters, enemies, action_result, result_damage):
        self.screen = screen
        self.manager = pygame_gui.UIManager(screen.get_size())

        # Options
        self.options = ['Attack', 'Magic', 'Flee', 'Skip', 'Scan']
        self.current_option_index = 0

            
        self.current_magic_option_index = 0
        self.cursor_symbol = ">"
        

        # Key Pressed State
        self.key_pressed = False
        self.show_magic = False
        self.show_enemy_boxes = False
        self.show_character_boxes = False
        self.show_dead_character_boxes = False
        self.selected_action_option = None
        self.selected_entity_option = None
        self.selected_magic = False

        # UITextBoxes
        self.menu_option_boxes = []
        self.magic_option_boxes = []
        self.enemy_options = []
        self.enemy_option_boxes = []
        self.character_infos = []
        self.character_options = []
        self.character_option_boxes = []
        self.dead_character_options = []
        self.dead_character_option_boxes = []


        self.update_magic_options(player_characters[0].magic_options)
        self.update_enemy_options(enemies)
        self.update_character_options(player_characters)


        # Initialize menu options
        for i, option in enumerate(self.options):
            cursor = self.cursor_symbol if i == self.current_option_index else " "
            text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((self.screen.get_width()/8, (self.screen.get_height()/1.9) + i * 30), (100, 30)),
                manager=self.manager,
                html_text=f"{cursor} {option}"
            )
            self.menu_option_boxes.append(text)

        # Initialize character information
        for i, character in enumerate(player_characters):
            character_info_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((i * 150, self.screen.get_height() - 100), (150, 110)),
                manager=self.manager,
                html_text=f"Name: {character.name}<br>Health: {character.health}<br>Magic: {character.magic_points}"
            )
            self.character_infos.append(character_info_text)


        # Initialize UI elements for turn counter, characters turn, action, and scan text
        self.turn_counter_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.screen.get_width()/40, 40), (100, 30)),
            manager=self.manager,
            html_text=f"Turn: {len(player_characters)}"
        )
        self.characters_turn = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.screen.get_width()/40, 10), (200, 30)),
            manager=self.manager,
            html_text=f"Whose Turn: {player_characters[0].name}"
        )
        self.action = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.screen.get_width()/2, 10), (300, 30)),
            manager=self.manager,
            html_text=f"{action_result} {result_damage}"
        )
        self.action.hide()
        self.action_start_time = 0
        self.action_duration = 3000

        self.scan_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((self.screen.get_width()/2.5, self.screen.get_height()/4), (200, 120)),
            manager=self.manager,
            html_text=f""
        )
        self.scan_text.hide()
        self.scan_start_time = 0
        self.scan_duration = 3000


    def handle_input(self):
        keys = pygame.key.get_pressed()

        if self.selected_action_option and self.selected_entity_option:
            self.selected_action_option = None
            self.selected_entity_option = None

        if not self.key_pressed:
            if not (self.show_enemy_boxes or self.show_character_boxes or self.show_dead_character_boxes):
                if not self.show_magic:
                    self.handle_menu_input(keys)
                else:
                    self.handle_magic_input(keys)
            else:
                if self.show_enemy_boxes:
                    self.handle_enemy_input(keys)
                elif self.show_character_boxes:
                    self.handle_character_input(keys)
                elif self.show_dead_character_boxes:
                    self.handle_dead_character_input(keys)
        else:
            if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_SPACE] or keys[pygame.K_a]):
                self.key_pressed = False

        return self.selected_action_option, self.selected_entity_option


    def handle_menu_input(self, keys):
        self.handle_menu_navigation(keys)
        selected_option = self.handle_menu_selection(keys)

        if selected_option == 'Attack':
            self.selected_action_option = selected_option
            self.show_enemy_options()
        elif selected_option == 'Flee':
            self.selected_action_option = selected_option
            self.selected_entity_option = 1
        elif selected_option == 'Magic':
            self.selected_magic = True
            self.show_magic_menu()
        elif selected_option == 'Skip':
            self.selected_action_option = selected_option
            self.selected_entity_option = 1
        elif selected_option == 'Scan':
            self.selected_action_option = selected_option
            self.show_enemy_options()


    def handle_magic_input(self, keys):
        self.handle_magic_navigation(keys)
        selected_option=self.handle_magic_selection(keys)
        if selected_option == 'Healing':
            self.selected_action_option = selected_option
            self.show_character_options()
        elif selected_option == 'Revive':
            if self.dead_character_options:  # if characters are dead
                self.selected_action_option = selected_option
                self.show_dead_character_options()
        elif selected_option in ['Fire', 'Water', 'Lightning', 'Earth']:
            self.selected_action_option = selected_option
            self.show_enemy_options()
        elif keys[pygame.K_a]:
            self.key_pressed = True
            self.remove_magic_menu()
            self.selected_magic = not self.selected_magic


    def handle_enemy_input(self, keys):
        self.handle_enemy_navigation(keys)
        selected_option = self.handle_enemy_selection(keys)
        if selected_option:
            self.selected_entity_option = selected_option
            self.remove_enemy_options()
            if self.selected_magic:
                self.remove_magic_menu()
                self.selected_magic = not self.selected_magic
        elif keys[pygame.K_a]:
            self.key_pressed = True
            self.remove_enemy_options()


    def handle_character_input(self, keys):
        self.handle_character_navigation(keys)
        selected_option = self.handle_character_selection(keys)
        if selected_option:
            self.selected_entity_option = selected_option
            self.remove_character_options()
            if self.selected_magic:
                self.remove_magic_menu()
                self.selected_magic = not self.selected_magic
        elif keys[pygame.K_a]:
            self.key_pressed = True
            self.remove_character_options()


    def handle_dead_character_input(self, keys):
        self.handle_dead_character_navigation(keys)
        selected_option = self.handle_dead_character_selection(keys)
        if selected_option:
            self.selected_entity_option = selected_option
            self.remove_dead_character_options()
            if self.selected_magic:
                self.remove_magic_menu()
                self.selected_magic = not self.selected_magic
        elif keys[pygame.K_a]:
            self.key_pressed = True
            self.remove_dead_character_options()



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
    
    def handle_character_navigation(self,keys):
            if keys[pygame.K_w]:
                self.current_character_option_index = (self.current_character_option_index - 1) % len(self.character_options)
                self.key_pressed = True
            elif keys[pygame.K_s]:
                self.current_character_option_index = (self.current_character_option_index + 1) % len(self.character_options)
                self.key_pressed = True
        
    
    def handle_character_selection(self, keys):
        if keys[pygame.K_SPACE]:
            selected_option = self.character_options[self.current_character_option_index]
            self.key_pressed = True
            return selected_option #return character object
    

    def show_character_options(self):
        self.current_character_option_index = 0
        self.show_character_boxes = not self.show_character_boxes
        for character_text in self.character_option_boxes:
            character_text.show()

    def remove_character_options(self):
        self.show_character_boxes = not self.show_character_boxes
        for character_text in self.character_option_boxes:
            character_text.hide()

    def handle_dead_character_navigation(self,keys):
            if keys[pygame.K_w]:
                self.current_dead_character_option_index = (self.current_dead_character_option_index - 1) % len(self.dead_character_options)
                self.key_pressed = True
            elif keys[pygame.K_s]:
                self.current_dead_character_option_index = (self.current_dead_character_option_index + 1) % len(self.dead_character_options)
                self.key_pressed = True
        
    
    def handle_dead_character_selection(self, keys):
        if keys[pygame.K_SPACE]:
            selected_option = self.dead_character_options[self.current_dead_character_option_index]
            self.key_pressed = True
            return selected_option #return character object
    
    def show_dead_character_options(self):
        self.current_dead_character_option_index = 0
        self.show_dead_character_boxes = not self.show_dead_character_boxes
        for character_text in self.dead_character_option_boxes:
            character_text.show()

    def remove_dead_character_options(self):
        self.show_dead_character_boxes = not self.show_dead_character_boxes
        for character_text in self.dead_character_option_boxes:
            character_text.hide()
        
    
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

    def update_enemy_options(self, alive_enemies):
        self.enemy_option_boxes = []
        self.enemy_options = []
        for i, enemy in enumerate(alive_enemies):
            cursor = self.cursor_symbol if i == 0 else " "
            enemy_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((self.screen.get_width()/2.45, (self.screen.get_height()/1.9) + i * 30), (200, 30)),
                manager=self.manager,
                html_text=f"{cursor} {enemy.enemy_type} {enemy.id_number}"
            )
            self.enemy_options.append(enemy)
            self.enemy_option_boxes.append(enemy_text)
            enemy_text.hide()
    

    def update_character_options(self, alive_characters):
        self.character_option_boxes = []
        self.character_options = []
        for i, character in enumerate(alive_characters):
            cursor = self.cursor_symbol if i == 0 else " "
            character_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((self.screen.get_width()/2.45, (self.screen.get_height()/1.9) + i * 30), (200, 30)),
                manager=self.manager,
                html_text=f"{cursor} {character.name}"
            )
            self.character_options.append(character)
            self.character_option_boxes.append(character_text)
            character_text.hide()

    def update_dead_character_options(self, dead_characters):
        self.dead_character_option_boxes = []
        self.dead_character_options = []
        for i, character in enumerate(dead_characters):
            cursor = self.cursor_symbol if i == 0 else " "
            dead_character_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((self.screen.get_width()/2.45, (self.screen.get_height()/1.9) + i * 30), (200, 30)),
                manager=self.manager,
                html_text=f"{cursor} {character.name}"
            )
            self.dead_character_options.append(character)
            self.dead_character_option_boxes.append(dead_character_text)
            dead_character_text.hide()

    def update_magic_options(self,player_magic):
        self.magic_option_boxes = []
        self.magic_options = []
        # Initialize player magic options
        for i, magic_option in enumerate(player_magic):
            cursor = self.cursor_symbol if i == self.current_magic_option_index else " "
            magic_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((self.screen.get_width()/4, (self.screen.get_height()/1.9) + i * 30), (125, 30)),
                manager=self.manager,
                html_text=f"{cursor} {magic_option}"
            )
            self.magic_options.append(magic_option)
            self.magic_option_boxes.append(magic_text)
            magic_text.hide()

        


    def render(self, alive_characters, dead_characters, player_characters, enemies, num_of_player_turns,
           character_taking_action, result, damage, action_selected):
        # Render the menu options
        for option_box, option in zip(self.menu_option_boxes, self.options):
            cursor = self.cursor_symbol if option_box == self.menu_option_boxes[self.current_option_index] else " "
            option_box.set_text(f"{cursor} {option}")

        if self.show_magic:
            # Render the magic menu options
            for magic_box, magic_option in zip(self.magic_option_boxes, self.magic_options):
                cursor = self.cursor_symbol if magic_box == self.magic_option_boxes[self.current_magic_option_index] else " "
                magic_box.set_text(f"{cursor} {magic_option}")

        # Render character information
        for character_info_text, character in zip(self.character_infos, player_characters):
            character_info_text.set_text(f"Name: {character.name}<br>Health: {character.health}<br>Magic: {character.magic_points}")

        # Render alive character options
        if self.show_character_boxes:
            for character_box, character in zip(self.character_option_boxes, alive_characters):
                cursor = self.cursor_symbol if character_box == self.character_option_boxes[self.current_character_option_index] else " "
                character_box.set_text(f"{cursor} {character.name}")

        # Render enemy options
        if self.show_enemy_boxes:
            for enemy_box, enemy in zip(self.enemy_option_boxes, enemies):
                cursor = self.cursor_symbol if enemy_box == self.enemy_option_boxes[self.current_enemy_option_index] else " "
                enemy_box.set_text(f"{cursor} {enemy.enemy_type} {enemy.id_number}")

        # Render dead character options
        if self.show_dead_character_boxes:
            for dead_character_box, dead_character in zip(self.dead_character_option_boxes, dead_characters):
                cursor = self.cursor_symbol if dead_character_box == self.dead_character_option_boxes[self.current_dead_character_option_index] else " "
                dead_character_box.set_text(f"{cursor} {dead_character.name}")

        self.turn_counter_text.set_text(f"Turns: {num_of_player_turns}")
        self.characters_turn.set_text(f"Current Turn: {character_taking_action.name}")

        self.render_action_result(result, damage, action_selected)

        self.hide_element_after_duration(self.action, self.action_start_time, self.action_duration)
        self.hide_element_after_duration(self.scan_text, self.scan_start_time, self.scan_duration)

        self.manager.update(pygame.time.get_ticks() / 1000.0)
        self.manager.draw_ui(self.screen)


    def render_action_result(self, result, damage, action_selected):
        if action_selected:
            if action_selected == 'Skip':
                self.action.set_text(f"{action_selected} {result}")
                self.action.show()
                self.action_start_time = pygame.time.get_ticks()
            elif action_selected == 'Scan':
                self.scan_text.set_text(f"{damage.enemy_type} {damage.id_number}<br>{damage.health}/{damage.max_health}<br>Weakness: {damage.weakness}<br>Strength: {damage.strength}")
                self.scan_text.show()
                self.scan_start_time = pygame.time.get_ticks()
            elif action_selected == 'Revived':
                self.action.set_text(f"{action_selected} {damage}")
                self.action.show()
                self.action_start_time = pygame.time.get_ticks()
            else:
                # For magic and attack options
                self.action.set_text(f"{action_selected} Damage: {damage}")
                self.action.show()
                self.action_start_time = pygame.time.get_ticks()
    
    def hide_element_after_duration(self, element, start_time, duration):
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time >= duration:
            element.hide()

