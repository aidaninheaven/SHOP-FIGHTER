import pygame
from fighter import Fighter

projectiles = []

print(Fighter)

pygame.init()

#create game window
screenWidth = 1000
screenHeight = 600

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Shop Fighter II")

#set frame rate
clock = pygame.time.Clock()
FPS = 60


#load background image
bgImage = pygame.image.load("assets/images/background/placeholderBG.jfif").convert_alpha()


#function for drawing background

def drawBG():
    
    scaledBG = pygame.transform.scale(bgImage, (screenWidth, screenHeight))
    screen.blit(scaledBG, (0,0))


#create 2 instances of fighters
fighter1 = Fighter(200, 310)
fighter2 = Fighter(700, 310)

#game loop
run = True

while run == True:

    clock.tick(FPS)

    #draw background
    drawBG()

    #move fighters
    fighter1.move(screenWidth, screenHeight, screen, fighter2)
    

    #draw fighters
    fighter1.draw(screen)
    fighter2.draw(screen)

    #event handler
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            run = False

    #update display
    pygame.display.update()


#exit pygame
pygame.quit()
