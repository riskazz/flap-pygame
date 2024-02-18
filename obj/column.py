import configs
import assets
from layer import Layer

import pygame.sprite
import random


class Column(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self.sprite = assets.get_sprite("pipe-green")
        self.sprites_rect = self.sprite.get_rect()
        self._layer = Layer.OBSTACLE
        self.gap = 90

        self.pipe_bottom = self.sprite
        self.pipe_bottom_rect = self.pipe_bottom.get_rect(topleft=(0, self.sprites_rect.height + self.gap))

        self.pipe_top = pygame.transform.flip(self.sprite, False, True)
        self.pipe_top_rect = self.pipe_top.get_rect(topleft=(0, 0))

        self.image = pygame.surface.Surface((self.sprites_rect.width, self.sprites_rect.height * 2 + self.gap), pygame.SRCALPHA)
        self.image.blit(self.pipe_bottom, self.pipe_bottom_rect)
        self.image.blit(self.pipe_top, self.pipe_top_rect)

        sprite_floor_height = assets.get_sprite("floor").get_rect().height
        min_y = 100
        max_y = configs.screen_height - sprite_floor_height - 110
        
        self.rect = self.image.get_rect(midleft=(configs.screen_width, random.uniform(min_y, max_y)))
        self.mask = pygame.mask.from_surface(self.image)

        self.passed = False
        self.mask = pygame.mask.from_surface(self.image)

        super().__init__(*groups)

    def update(self):
        self.rect.x -= 2

        if self.rect.right <= 0:
            self.kill()

    def is_passed(self):
        if self.rect.x < 50 and not self.passed:
            self.passed = True
            return True
        return False 
