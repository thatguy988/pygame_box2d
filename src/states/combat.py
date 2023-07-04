import pygame
from pygame.locals import *

class CombatState:
    def __init__(self, screen, key_pressed):
        self.screen = screen
        self.key_pressed = key_pressed

    def get_next_state(self):
        return self.handle_input()  

    def handle_input(self):
        keys = pygame.key.get_pressed()
        

        if keys[K_q]:
            return 3, True
        
        return None, self.key_pressed

    def update(self):
        pass


    def render(self):
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)
        text = font.render("In Combat State", True, text_color)
        text_rect = text.get_rect()
        text_rect.center = self.screen.get_rect().center
        self.screen.blit(text, text_rect)
