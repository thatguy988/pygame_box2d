import pygame


class Camera:
    def __init__(self, screen, level_width, level_height, camera_speed):
        self.screen = screen
        self.level_width = level_width
        self.level_height = level_height
        self.camera_speed = camera_speed
        self.camera = pygame.math.Vector2(0, 0)

    def update(self, character):
        # Smoothly adjust the camera position to center the player
        camera_target = pygame.math.Vector2(
            character.x - self.screen.get_width() / 2,
            character.y - self.screen.get_height() / 2
        )

        self.camera += (camera_target - self.camera) * self.camera_speed
        self.camera.x = max(0, min(self.camera.x, self.level_width - self.screen.get_width()))
        self.camera.y = max(0, min(self.camera.y, self.level_height - self.screen.get_height()))

    def apply(self, rect):
        return pygame.Rect(rect.x - self.camera.x, rect.y - self.camera.y, rect.width, rect.height)

    def render(self, game_objects):
        self.screen.fill((0, 0, 0))  # Clear the screen

        rendered_objects = []
        for game_object in game_objects:
            rect = self.apply(game_object[0])  # Extract the rect from the tuple
            rendered_objects.append((rect, game_object[1]))  # Create a new tuple with the rect and color

        # Render the rendered_objects using the camera view
        for rendered_object in rendered_objects:
            pygame.draw.rect(self.screen, rendered_object[1], rendered_object[0])

