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

#define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255) 

#define fighter variables. SIZE IS FOR PLACEHOLERS
e3000Size = 29
e3000Data = [e3000Size]

wizardSize = 29
wizardData = [wizardSize]


#load background image
bgImage = pygame.image.load("assets/images/background/placeholderBG.jfif").convert_alpha()

#load spritesheets

e3000Sheet = pygame.image.load("assets/images/e3000/PlaceHolderFighter.png").convert_alpha()
wizardSheet = pygame.image.load("assets/images/wizard/PlaceHolderFighter.png").convert_alpha()

#define number of steps in each animation
e3000AnimationSteps = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
wizardAnimationSteps = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]



#function for drawing background

def drawBG():
    
    scaledBG = pygame.transform.scale(bgImage, (screenWidth, screenHeight))
    screen.blit(scaledBG, (0,0))

#function for drawing fighter health bars
def drawHealthBar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y -2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


#create 2 instances of fighters
fighter1 = Fighter(200, 310, e3000Data, e3000Sheet, e3000AnimationSteps)
fighter2 = Fighter(700, 310, wizardData, wizardSheet, wizardAnimationSteps)

#game loop
run = True

while run == True:

    clock.tick(FPS)

    #draw background
    drawBG()

    #show player stats
    drawHealthBar(fighter1.health, 20, 20)
    drawHealthBar(fighter2.health, 580, 20)

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
