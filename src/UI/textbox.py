class TextBox:
    def __init__(self, position, size, font, color):
        self.position = position
        self.size = size
        self.font = font
        self.color = color
        self.text = ""

    def set_text(self, text):
        self.text = text

    def render(self, screen):
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, self.position)
