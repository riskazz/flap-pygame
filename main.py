import pygame

import sys


import configs
import assets
from obj.background import Background
from obj.button import Button
from obj.floor import Floor
from obj.column import Column
from obj.bird import Bird
from obj.start import GameStartMsg
from obj.over import GameOverMsg
from obj.score import Score

pygame.init()

# change default icon
new_icon = pygame.image.load('flappybird.ico')

pygame.display.set_icon(new_icon)

# create screen/game window
screen = pygame.display.set_mode((configs.screen_width, configs.screen_height))
pygame.display.set_caption("Flap Pygame")

# create clock
clock = pygame.time.Clock()

# loading media modules
assets.load_sprites()
assets.load_audios()
sprites = pygame.sprite.LayeredUpdates()

# create play buttons
# start_button = Button()

# initiate game loops
run = True
gameStart = False
gameOver = False

def game_loop():
    # add the background
    Background(0, sprites)
    Background(1, sprites)

    # add the floor
    Floor(0, sprites)
    Floor(1, sprites)

    # add column pipes
    column_timer = 1700
    pygame.time.set_timer(pygame.USEREVENT, column_timer)

    # add bird
    bird = Bird(sprites)

    # start game msg
    gsm = GameStartMsg(sprites)
    
    return bird, gsm, Score(sprites), column_timer


bird, gsm, score, column_timer = game_loop()


while run:
    clock.tick(configs.FPS)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                assets.play_audio("wing")
                gameStart = True
                gsm.kill()
            if event.key == pygame.K_ESCAPE:
                gameOver = False
                gameStart = False
                sprites.empty()
                bird, gsm, score, column_timer = game_loop()
        if event.type == pygame.QUIT:
            run = False 
        if event.type == pygame.USEREVENT:
            Column(sprites)
        if not gameOver:
            bird.handle_event(event)

    screen.fill(0)

    sprites.draw(screen)
        
    for sprite in sprites:
        if type(sprite) is Column and sprite.is_passed():
            score.value += 1 # add score every column passing
            assets.play_audio("point")
            if score.value > 7:
                column_timer -= 50 # decrease column timer every successful passing
                pygame.time.set_timer(pygame.USEREVENT, column_timer)   

    if  not  gameOver:
        sprites.update()

    if bird.check_collision(sprites) and not gameOver:
        gameOver = True
        gameStart = False
        GameOverMsg(sprites)
        assets.play_audio("hit")
        gsm.kill()
        
    pygame.display.flip()

pygame.quit()