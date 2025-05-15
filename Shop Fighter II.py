import pygame
import time
import random
import math
from fighter import Fighter



pygame.init()

#START for copying into menu and game

#create game window
screenWidth = 960   #960
screenHeight = 720   #720

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Shop Fighter II")

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#define colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

#define game variables
introCount = 0 #3
lastCountUpdate = pygame.time.get_ticks()
score = [0, 0] #player scores. [P1, P2]
roundOver = False
roundOverCooldown = 2000

#define fighter variables. SIZE IS FOR PLACEHOLERS
e3000Size = 162
e3000Scale = 4
#prolly need to change this when we get new sprites
e3000Offset = [72, 56]
e3000Data = [e3000Size, e3000Scale, e3000Offset]

wizardSize = 250
wizardScale = 3
#prolly need to change this when we get new sprites
wizardOffset = [112, 107]
wizardData = [wizardSize, wizardScale, wizardOffset]


#load background image
bgImage = pygame.image.load("assets/images/background/placeholderBG.jfif").convert_alpha()

#load spritesheets
e3000Sheet = pygame.image.load("assets/images/e3000/warrior.png").convert_alpha()
wizardSheet = pygame.image.load("assets/images/wizard/wizard.png").convert_alpha()

#load victory image
victoryImg = pygame.image.load("assets/images/ui/victory.png")

#load health bar
hpBar = pygame.image.load("assets/images/ui/healthbar.png")

#define number of steps in each animation
e3000AnimationSteps = [10, 8, 1, 7, 7, 3, 7] #7, 7, 3, 3, 10, 3, 7, 7, 8, 8
wizardAnimationSteps = [8, 8, 1, 8, 8, 3, 7]

#define font
countFont = pygame.font.Font("assets/fonts/turok.ttf", 80)
scoreFont = pygame.font.Font("assets/fonts/turok.ttf", 30)

#function for drawing text
def drawText(text, font, textColor, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img, (x, y))

#function for drawing background

def drawBG():
    
    scaledBG = pygame.transform.scale(bgImage, (screenWidth, screenHeight))
    screen.blit(scaledBG, (0,0))

#function for drawing fighter health bars
def drawHealthBar(health, x, y, invert):
    ratio = health / 100
    #pygame.draw.rect(screen, WHITE, (x - 2, y -2, 404, 34)) #404, 34

    scaledhpBar = pygame.transform.scale(hpBar, (550, 48))

    scaledhpBar = pygame.transform.flip(scaledhpBar, invert, False)

    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

    if invert == False:

        screen.blit(scaledhpBar, (x - 12, y - 8))

    else:

        screen.blit(scaledhpBar, (x - 138, y - 8))


#create 2 instances of fighters
fighter1 = Fighter(1, 200, 310, False, e3000Data, e3000Sheet, e3000AnimationSteps)
fighter2 = Fighter(2, 700, 310, True, wizardData, wizardSheet, wizardAnimationSteps)

#game loop
run = True

while run == True:

    clock.tick(FPS)

    #draw background
    drawBG()

    #show player stats
    drawHealthBar(fighter1.health, 20, 20, False)
    drawHealthBar(fighter2.health, 540, 20, True)
    drawText("P1: " + str(score[0]), scoreFont, RED, 20, 60)
    drawText("P2: " + str(score[1]), scoreFont, RED, 580, 60)

    #update countdown
    if introCount <= 0:
        #move fighters
        fighter1.move(screenWidth, screenHeight, screen, fighter2, roundOver)
        fighter2.move(screenWidth, screenHeight, screen, fighter1, roundOver)
    
    else:
        #display count timer
        drawText(str(introCount), countFont, RED, screenWidth / 2, screenHeight / 3)

        #update countdown
        if (pygame.time.get_ticks() - lastCountUpdate) >= 1000:
            introCount -=1
            lastCountUpdate = pygame.time.get_ticks()
        

 
    #update fighters
    fighter1.update(1)
    fighter2.update(2)

    

    #draw fighters
    fighter1.draw(screen)
    fighter2.draw(screen)

    #check for player defeat
    if roundOver == False:
        if fighter1.alive == False:
            score[1] += 1
            roundOver = True
            roundOverTime = pygame.time.get_ticks()

        elif fighter2.alive == False:
            score[0] += 1
            roundOver = True
            roundOverTime = pygame.time.get_ticks()

    else:
        #display victory image
        screen.blit(victoryImg, (360, 150))

        if pygame.time.get_ticks() - roundOverTime > roundOverCooldown:
            roundOver = False
            introCount = 4

            fighter1 = Fighter(1, 200, 310, False, e3000Data, e3000Sheet, e3000AnimationSteps)
            fighter2 = Fighter(2, 700, 310, True, wizardData, wizardSheet, wizardAnimationSteps)
            

    #event handler
    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            run = False

    #update display
    pygame.display.update()


#exit pygame
pygame.quit()

#END
