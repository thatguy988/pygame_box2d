
class Character:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def move(self,character_body):
        # Update enemy position based on the Box2D body
        self.x = character_body.position.x
        self.y = character_body.position.y
        

    