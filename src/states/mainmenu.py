import pygame
import sys
from pygame.locals import *



class MainMenuState:
    def __init__(self, screen):
        self.screen = screen
        self.selected_option = 0
        self.options = ["Start Game", "Load Game", "Quit"]
        self.cursor_symbol =  ">"
        self.key_pressed = False  #track key press
    
    def get_next_state(self):
        return self.handle_input()


    def handle_input(self):
        keys = pygame.key.get_pressed()

        if not self.key_pressed:  # Check if key is not already pressed
            if keys[K_w]:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                self.key_pressed = True
            elif keys[K_s]:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                self.key_pressed = True
        else:
            if not (keys[K_w] or keys[K_s]):
                self.key_pressed = False
        if keys[K_SPACE]:  # Check for spacebar key press
            if self.options[self.selected_option] == "Start Game":
                return 3 # Transition to the PlatformingState
            if self.options[self.selected_option] == "Quit":
                pygame.quit()  # Quit the Pygame program
                sys.exit()  # Terminate the Python program

        return None

    def update(self):
        self.handle_input()

    def render(self):
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)

        # Render options
        for index, option in enumerate(self.options):
            text = font.render(option, True, text_color)
            text_rect = text.get_rect()
            text_rect.x = self.screen.get_rect().centerx - text_rect.width // 2
            text_rect.y = 200 + index * 50

            cursor_rect = font.render(self.cursor_symbol, True, text_color).get_rect()
            cursor_rect.x = text_rect.left - cursor_rect.width - 10
            cursor_rect.centery = text_rect.centery

            if index == self.selected_option:
                self.screen.blit(font.render(self.cursor_symbol, True, (0, 255, 0)), cursor_rect)
            

            self.screen.blit(text, text_rect)
