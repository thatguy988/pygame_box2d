
import pygame
from pygame_gui.elements import UITextBox
from pygame_gui.core import UIContainer

class TextBox:
    def __init__(self, position, size, font, color, manager):
        self.position = position
        self.size = size
        self.font = font
        self.color = color
        self.text = ""

        # Create a UIContainer to hold the UITextBox
        self.container = UIContainer(relative_rect=pygame.Rect(position, size), manager=manager)

        # Create the UITextBox element
        self.textbox = UITextBox(html_text="", relative_rect=pygame.Rect((0, 0), size),
                                 manager=manager, container=self.container)

    def set_text(self, text):
        self.text = text
        self.textbox.html_text = text  # Update the text of the UITextBox

    def render(self, screen):
        # No need to manually render the text box in this method
        pass
