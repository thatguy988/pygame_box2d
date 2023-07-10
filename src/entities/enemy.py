class Enemy:
    enemy_data = {
        "slime": {
            "health": 20,
            "magic_points":30,
            "strength": "Lightning",
            "weakness": "Earth",
            "attack_power": 5
        }
        
    }

    def __init__(self, x, y, width, height, enemy_type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.enemy_type = enemy_type
        data = Enemy.enemy_data.get(enemy_type, {})
        self.health = data.get("health")
        self.magic_points = data.get("magic_points")
        self.strength = data.get("strength")
        self.weakness = data.get("weakness")
        self.attack_power = data.get("attack_power")
        self.id_number = None
        self.alive = True

    def move(self, enemy_body):
        # Update enemy position based on the Box2D body
        self.x = enemy_body.position.x
        self.y = enemy_body.position.y

    @staticmethod
    def create_enemy(x_position, y_position, enemy_type):
        x = x_position
        y = y_position
        width = 50
        height = 50

        return Enemy(x, y, width, height, enemy_type)
