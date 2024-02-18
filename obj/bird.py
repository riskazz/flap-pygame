import pygame.sprite


import assets
import configs
from layer import Layer
from obj.column import Column
from obj.floor import Floor


class Bird(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self.images = [
            (assets.get_sprite("redbird-upflap")),
            (assets.get_sprite("redbird-midflap")),
            (assets.get_sprite("redbird-downflap"))]

        self._layer = Layer.PLAYER
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(configs.screen_width/2, 250))
        self.mask = pygame.mask.from_surface(self.image)

        self.flap = 0
        self.rotation_angle = 0
        self.any_key_pressed = False  # Flag to track if any key is pressed

        super().__init__(*groups)

    def update(self):
        self.images.insert(0, self.images.pop())
        self.image = self.images[0]

        if self.any_key_pressed:  # Apply gravity ONLY IF any key is pressed
            self.flap += configs.gravity
            self.rect.y += self.flap

            # Update rotation angle based on flap movement
            self.rotation_angle = min(max(self.flap * -2, -90), 45)  # Clamp rotation angle between -90 and 45 degrees

            # Load different bird images based on flap movement
            if self.flap < 0:
                self.image = pygame.transform.rotate(self.images[0], self.rotation_angle)  # Redbird-upflap
            elif self.flap == 0:
                self.image = self.images[1]  # Redbird-midflap
            else:
                self.image = pygame.transform.rotate(self.images[2], self.rotation_angle)  # Redbird-downflap

            # Handle rotation when no key is pressed
            if self.flap == 0:
                self.rotation_angle = -45  # Rotate the bird image to face downwards
                self.image = pygame.transform.rotate(self.images[1], self.rotation_angle)  # Redbird-midflap

        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.any_key_pressed = True  # Set the flag to True when any key is pressed
            if event.key == pygame.K_SPACE:
                self.flap = 0
                self.flap -= 6
                
    def check_collision(self, sprites):
        for sprite in sprites:
            if (isinstance(sprite, (Column, Floor)) and sprite.mask.overlap(
                self.mask, (self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)) or self.rect.bottom < 0):
                return True

        return False
