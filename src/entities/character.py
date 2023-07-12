class Character:
    character_data = {
        "Player 1": {
            "health": 100,
            "magic_points": 50,
            "strength": "Fire",
            "weakness": "Water",
            "attack_power": 10
        },
        "Player 2": {
            "health": 60,
            "magic_points": 40,
            "strength": "Lightning",
            "weakness": "Earth",
            "attack_power": 15
        },
        "Player 3": {
            "health": 120,
            "magic_points": 80,
            "strength": "Water",
            "weakness": "Fire",
            "attack_power": 5
        },
        "Player 4": {
            "health": 150,
            "magic_points": 75,
            "strength": "Earth",
            "weakness": "Lightning",
            "attack_power": 10
        }
    }

    def __init__(self, x, y, width, height, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.alive = True

        data = Character.character_data.get(name, {})
        self.health = data.get("health")
        self.magic_points = data.get("magic_points")
        self.strength = data.get("strength")
        self.weakness = data.get("weakness")
        self.attack_power = data.get("attack_power")
        
        self.rect = None

    def move(self, character_body):
        # Update character position based on the Box2D body
        self.x = character_body.position.x
        self.y = character_body.position.y

    @staticmethod
    def create_character(x_position, y_position, name):
        x = x_position
        y = y_position
        width = 50
        height = 50

        return Character(x, y, width, height, name)

    def restore_health_and_magic(self):
        data = Character.character_data.get(self.name, {})
        self.health = data.get("health")
        self.magic_points = data.get("magic_points")
        self.alive = True

        

    