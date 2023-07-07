
class Character:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 100
        self.magic_points = 100
        self.name = "Player 1"
        
        self.strength = "Fire" 
        self.weakness = "Water"
        self.attack_power = 5
        
    def move(self,character_body):
        # Update enemy position based on the Box2D body
        self.x = character_body.position.x
        self.y = character_body.position.y

    @staticmethod
    def create_character(x_position,y_position):
        x = x_position  
        y = y_position  
        width = 50  
        height = 50  
        
        # Create and return a new character object
        return Character(x, y, width, height)

        

    