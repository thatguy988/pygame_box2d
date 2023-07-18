import pygame

class Platform:
    def __init__(self, x, y, width, height, tile):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)  # Create a pygame Rect
        self.tile_type = tile

    def move(self, body):
        # Update platform position based on the Box2D body
        self.x = body.position.x
        self.y = body.position.y

    @staticmethod
    def create_platform(x_position,y_position,tile):
        x=x_position
        y=y_position

        

        if tile == 50:
            width = 50
            height = 50
        elif tile == 49:
            width = 50
            height = 50
        return Platform(x,y,width,height,tile)
    
    def get_position(self):

        return self.x,self.y
        
    def get_tile_type(self):

        return self.tile_type
