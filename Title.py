# Example file showing a basic pygame "game loop"
import pygame
import time
import random
import math
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
titlebg=pygame.image.load("titlebg.png").convert_alpha()
title=pygame.image.load("SFIIPixelLogo.png").convert_alpha()
title=pygame.transform.scale_by(title,5)
setpanel=pygame.image.load("settingspanel.png").convert_alpha()
cursor=pygame.image.load("Cursor.png").convert_alpha()
running = True
pygame.display.set_caption("SHOP FIGHTER II")
textfont = pygame.font.SysFont("mssansserif",20)
for i in range(60):
    screen.fill("black")
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    time.sleep(0.01)
screen.fill("white")
pygame.display.flip()
time.sleep(0.1)

itr=20
for i in range(itr):
    titlex=297.5
    titley=100
    screen.fill("black")
    screen.blit(titlebg,(0,0))
    dir=random.randrange(-180,180)
    titlex=titlex+(math.sin(dir))*itr
    titley=titley+(math.cos(dir))*itr
    screen.blit(title,(titlex,titley))
    pygame.display.flip()
    time.sleep(0.01)
    itr=itr-1



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    screen.blit(titlebg,(0,0))
    screen.blit(title,(297.5,100))

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()