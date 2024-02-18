import pygame.sprite

import configs
import assets
from layer import Layer

class GameStartMsg(pygame.sprite.Sprite):
    def __init__(self, *groups):
        self._layer = Layer.UI
        self.image = assets.get_sprite("message")
        self.rect = self.image.get_rect(center=(configs.screen_width/2, 202))

        super().__init__(*groups)
