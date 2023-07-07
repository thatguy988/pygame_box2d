
import pygame
import pygame_gui

class CombatMenus:
    def __init__(self, screen):
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

        # UITextBoxes
        self.menu_option_boxes = []
        self.magic_option_boxes = []

        for i, option in enumerate(self.options):
            cursor = self.cursor_symbol if i == self.current_option_index else " "
            text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((100, 100 + i * 30), (200, 30)),
                manager=self.manager,
                html_text=f"{cursor} {option}"
            )
            self.menu_option_boxes.append(text)

        for i, magic_option in enumerate(self.magic_options):
            cursor = self.cursor_symbol if i == self.current_magic_option_index else " "
            magic_text = pygame_gui.elements.UITextBox(
                relative_rect=pygame.Rect((400, 100 + i * 30), (200, 30)),
                manager=self.manager,
                html_text=f"{cursor} {magic_option}"
            )
            self.magic_option_boxes.append(magic_text)
            magic_text.hide()

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if not self.key_pressed:
            # Handle menu navigation
            if not self.show_magic:
                if keys[pygame.K_w]:
                    self.key_pressed = True
                    self.current_option_index -= 1
                    if self.current_option_index < 0:
                        self.current_option_index = len(self.options) - 1
                elif keys[pygame.K_s]:
                    self.key_pressed = True
                    self.current_option_index += 1
                    if self.current_option_index >= len(self.options):
                        self.current_option_index = 0

                # Handle selecting menu option
                elif keys[pygame.K_SPACE]:
                    self.key_pressed = True
                    selected_option = self.options[self.current_option_index]
                    if selected_option == 'Magic':
                        self.show_magic_menu()
            else:  # navigate magic options
                if keys[pygame.K_w]:
                    self.key_pressed = True
                    self.current_magic_option_index -= 1
                    if self.current_magic_option_index < 0:
                        self.current_magic_option_index = len(self.magic_options) - 1
                elif keys[pygame.K_s]:
                    self.key_pressed = True
                    self.current_magic_option_index += 1
                    if self.current_magic_option_index >= len(self.magic_options):
                        self.current_magic_option_index = 0
                elif keys[pygame.K_a]:
                    self.key_pressed = True
                    self.remove_magic_menu()

        else:
            if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_SPACE] or keys[pygame.K_a]):
                self.key_pressed = False

    def show_magic_menu(self):
        self.current_magic_option_index = 0
        self.show_magic = True
        for magic_text in self.magic_option_boxes:
            magic_text.show()

    def remove_magic_menu(self):
        self.show_magic = False
        for magic_text in self.magic_option_boxes:
            magic_text.hide()

    def render(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))

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

        self.manager.update(pygame.time.get_ticks() / 1000.0)
        self.manager.draw_ui(self.screen)




