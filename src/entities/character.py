class Character:
    character_data = {
        "Player 1": {
            "health": 100,
            "magic_points": 50,
            "strength": "Fire",
            "weakness": "Water",
            "attack_power": 10,
            "magic_attack_power": 5,
            "healing_power": 5,
            "magic_options": ['Fire','Earth','Revive']
        },
        "Player 2": {
            "health": 60,
            "magic_points": 40,
            "strength": "Lightning",
            "weakness": "Earth",
            "attack_power": 15,
            "magic_attack_power": 5,
            "healing_power": 5,
            "magic_options": ['Healing','Revive']

        },
        "Player 3": {
            "health": 120,
            "magic_points": 80,
            "strength": "Water",
            "weakness": "Fire",
            "attack_power": 5,
            "magic_attack_power": 5,
            "healing_power": 5,
            "magic_options": ['Lightning','Healing','Revive']

        },
        "Player 4": {
            "health": 150,
            "magic_points": 75,
            "strength": "Earth",
            "weakness": "Lightning",
            "attack_power": 10,
            "magic_attack_power": 5,
            "healing_power": 5,
            "magic_options": ['Water','Earth']

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
        self.magic_attack_power = data.get("magic_attack_power")
        self.healing_power = data.get("healing_power")

        self.max_health = data.get("health")
        self.max_magic_points = data.get("magic_points")
        
        self.rect = None
        self.magic_options = data.get("magic_options")

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
        self.health = self.max_health
        self.magic_points = self.max_magic_points
        self.alive = True

        

    