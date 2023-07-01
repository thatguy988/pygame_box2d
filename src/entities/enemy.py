
class Enemy:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    #spawn enemies using value of 7 in element of array
    def move(self,enemy_body):
        # Update enemy position based on the Box2D body
        self.x = enemy_body.position.x
        self.y = enemy_body.position.y