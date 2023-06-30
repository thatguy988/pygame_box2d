import pygame
class Character:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.move_speed = .25

    def move_up(self):
        self.y -= self.move_speed

    def move_down(self):
        self.y += self.move_speed

    def move_left(self):
        self.x -= self.move_speed

    def move_right(self):
        self.x += self.move_speed

    
