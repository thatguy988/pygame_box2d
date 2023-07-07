
import pygame
import pygame_gui

class CombatMenus:
    def __init__(self, screen, character_health,character_magic_points,character_name,enemies):
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

        # UITextBoxes
        self.menu_option_boxes = []
        self.magic_option_boxes = []

        self.enemy_option_boxes = []

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
        self.character_name_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, screen.get_height() - 70), (200, 30)),
            manager=self.manager,
            html_text=f"Health: {character_name}"
        )
        # Render player character's health and magic points
        self.character_health_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, screen.get_height() - 50), (200, 30)),
            manager=self.manager,
            html_text=f"Health: {character_health}"
        )
        self.character_magic_text = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, screen.get_height() - 30), (200, 30)),
            manager=self.manager,
            html_text=f"Magic: {character_magic_points}"
        )
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


    def handle_input(self):
        keys = pygame.key.get_pressed()

        if not self.key_pressed:
            if not self.show_enemy_boxes:
                if not self.show_magic:
                    self.handle_menu_navigation(keys)
                    selected_option = self.handle_menu_selection(keys)
                    if selected_option == 'Attack':
                        self.show_enemy_options()
                    elif selected_option == 'Flee':
                        return selected_option
                    elif selected_option == 'Magic':
                        self.show_magic_menu()
                else:
                    self.handle_magic_navigation(keys)
                    selected_option = self.handle_magic_selection(keys)
                    if selected_option:
                        self.show_enemy_options()
                    elif keys[pygame.K_a]:
                        self.key_pressed = True
                        self.remove_magic_menu()
            else:
                self.handle_enemy_navigation(keys)
                selected_option=self.handle_enemy_selection(keys)
                if selected_option:
                    return selected_option
                elif keys[pygame.K_a]:
                    self.key_pressed = True
                    self.remove_enemy_options()

        else:
            if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_SPACE] or keys[pygame.K_a]):
                self.key_pressed = False

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

    def render(self,character_health, character_magic_points, character_name,enemies):

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
        self.character_health_text.set_text(f"Health: {character_health}")
        self.character_magic_text.set_text(f"Magic: {character_magic_points}")
        self.character_name_text.set_text(f"{character_name}")
        if self.show_enemy_boxes:
            for i, enemy in enumerate(enemies):
                cursor = self.cursor_symbol if i == self.current_enemy_option_index else " "
                text = self.enemy_option_boxes[i]
                text.set_text(f"{cursor} Enemy {enemy.id_number}")

        self.manager.update(pygame.time.get_ticks() / 1000.0)
        self.manager.draw_ui(self.screen)

        #return attack, enemy object 
        #return magic attack, enemy object



            # def handle_input(self):
    #     keys = pygame.key.get_pressed()

    #     if not self.key_pressed:
    #         # Handle menu navigation
    #         if not self.show_magic and not self.show_enemy_options:
    #             if keys[pygame.K_w]:
    #                 self.key_pressed = True
    #                 self.current_option_index -= 1
    #                 if self.current_option_index < 0:
    #                     self.current_option_index = len(self.options) - 1
    #             elif keys[pygame.K_s]:
    #                 self.key_pressed = True
    #                 self.current_option_index += 1
    #                 if self.current_option_index >= len(self.options):
    #                     self.current_option_index = 0
    #             # Handle selecting menu option
    #             elif keys[pygame.K_SPACE]:
    #                 self.key_pressed = True
    #                 selected_option = self.options[self.current_option_index]
    #                 if selected_option == 'Attack':
    #                     self.show_attack_options()
    #                 if selected_option == 'Flee':
    #                     return selected_option

    #                 if selected_option == 'Magic':
    #                     self.show_magic_menu()
                    
    #         elif self.show_magic and not self.show_enemy_options:  # navigate magic options
    #             if keys[pygame.K_w]:
    #                 self.key_pressed = True
    #                 self.current_magic_option_index -= 1
    #                 if self.current_magic_option_index < 0:
    #                     self.current_magic_option_index = len(self.magic_options) - 1
    #             elif keys[pygame.K_s]:
    #                 self.key_pressed = True
    #                 self.current_magic_option_index += 1
    #                 if self.current_magic_option_index >= len(self.magic_options):
    #                     self.current_magic_option_index = 0
    #             elif keys[pygame.K_SPACE]:
    #                 self.key_pressed=True
    #                 selected_option=self.magic_options[self.current_magic_option_index]
    #                 self.show_attack_options()
    #             elif keys[pygame.K_a]:
    #                 self.key_pressed = True
    #                 self.remove_magic_menu()
    #         elif not self.show_magic and self.show_enemy_options: #player selected attack now we select enemy
    #             print("selected attack option select what enemy to attack")
    #             if keys[pygame.K_a]:
    #                 self.key_pressed = True
    #                 self.remove_attack_options()
    #         elif self.show_magic and self.show_enemy_options:
    #             print("selected magic option attack enemy with magic")
    #             if keys[pygame.K_a]:
    #                 self.key_pressed = True
    #                 self.remove_attack_options()


    #     else:
    #         if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_SPACE] or keys[pygame.K_a]):
    #             self.key_pressed = False




