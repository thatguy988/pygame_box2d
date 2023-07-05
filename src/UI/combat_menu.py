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

        # Key Pressed State
        self.key_pressed = pygame.key.get_pressed()

    def handle_input(self):
        self.key_pressed = pygame.key.get_pressed()

        # Handle menu navigation
        if self.key_pressed[pygame.K_w]:
            self.current_option_index -= 1
            if self.current_option_index < 0:
                self.current_option_index = len(self.options) - 1
        elif self.key_pressed[pygame.K_s]:
            self.current_option_index += 1
            if self.current_option_index >= len(self.options):
                self.current_option_index = 0

        # Handle selecting menu option
        if self.key_pressed[pygame.K_SPACE]:
            selected_option = self.options[self.current_option_index]
            if selected_option == 'Magic':
                self.show_magic_menu()

    def show_magic_menu(self):
        self.current_magic_option_index = 0

    def render(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))

        # Render the menu options
        for i, option in enumerate(self.options):
            text = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((100, 100 + i * 30), (200, 30)),
                                                 manager=self.manager,
                                                 html_text=option)

            if i == self.current_option_index:
                text.set_active_effect('highlight')

        # Render the magic menu options
        if self.options[self.current_option_index] == 'Magic':
            for i, magic_option in enumerate(self.magic_options):
                text = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((400, 100 + i * 30), (200, 30)),
                                                     manager=self.manager,
                                                     html_text=magic_option)

                if i == self.current_magic_option_index:
                    text.set_active_effect('highlight')

        self.manager.update(pygame.time.get_ticks() / 1000.0)
        self.manager.draw_ui(self.screen)
