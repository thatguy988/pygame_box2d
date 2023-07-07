
class Enemy:
    def __init__(self, x, y, width, height, enemy_type, strength, weakness, attack_power):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.enemy_type = enemy_type
        self.health = 20
        self.magic_points = 30
        self.strength = strength
        self.weakness = weakness
        self.attack_power = attack_power
        self.id_number = None

        
    #spawn enemies using value of 7 in element of array
    def move(self,enemy_body):
        # Update enemy position based on the Box2D body
        self.x = enemy_body.position.x
        self.y = enemy_body.position.y


    @staticmethod
    def create_enemy(x_position, y_position, enemy_type):
        x = x_position
        y = y_position
        width = 50  
        height = 50
        strength = Enemy.define_strength(enemy_type)  
        weakness = Enemy.define_weakness(enemy_type)
        attack_power = Enemy.define_attack_power(enemy_type)

        # Create and return a new enemy object
        return Enemy(x, y, width, height, enemy_type, strength, weakness, attack_power)
    


    def define_strength(enemy_type):
        if (enemy_type == "slime"):
            return "thunder"
        

    def define_weakness(enemy_type):
        if (enemy_type == "slime"):
            return "earth"


    def define_attack_power(enemy_type):
        if (enemy_type == "slime "):
            return 5
        
        