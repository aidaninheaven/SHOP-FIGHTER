import pygame

from projectiles import Projectile

class Fighter():
    
    def __init__(self, x, y, flip, data, spriteSheet, animationSteps):

        self.size = data[0]
        self.imageScale = data[1]
        self.offset = data[2]

        self.flip = flip

        self.animationList = self.loadImages(spriteSheet, animationSteps)
        self.action = 0 #0: idle   #1: run     #2: jump    #3: attack1    #4: attack2    #5: hit    #6: death
        self.frameIndex = 0
        self.image = self.animationList[self.action][self.frameIndex]
        self.updateTime = pygame.time.get_ticks()

        self.rect = pygame.Rect((x, y, 80, 180))

        #Y velocity
        self.velY = 0
        self.running = False
        self.jump = False
        self.attacking = False
       

        #which attack is being used
        self.attackType = 0

        self.health = 100


    def loadImages(self, spriteSheet, animationSteps):

        #extract images from spritesheet
        animationList = []

        for y, animation in enumerate(animationSteps):

            tempImgList = []

            for x in range(animation):
                tempImg = spriteSheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                
                tempImgList.append(pygame.transform.scale(tempImg, (self.size * self.imageScale, self.size * self.imageScale)))

            animationList.append(tempImgList)

        return animationList




    def move(self, screenWidth, screenHeight, surface, target):

        speed = 10
        gravity = 2
        dx = 0
        dy = 0
        self.running = False
        self.attackType = 0

        #get keypresses
        key = pygame.key.get_pressed()

        #can only perform other actions if not currently attacking
        if self.attacking == False:

            #movement
            if key[pygame.K_a]:
                dx = -speed
                self.facingLeft = True
                self.running = True

            if key[pygame.K_d]:
                dx = speed
                self.facingLeft = False
                self.running = True
            #jump
            if key[pygame.K_w] and self.jump == False:
                self.velY = -30
                self.jump = True

            #attack
            if key[pygame.K_r] or key[pygame.K_t] or key[pygame.K_f]:

                self.attack(surface, target)
                
                #determine which attack was used
                if key[pygame.K_r]:
                    self.attackType = 1
                if key[pygame.K_t]:
                    self.attackType = 2
                if key[pygame.K_f]:
                    self.attackType = 3

        print(self.attackType)

        #apply gravity

        self.velY += gravity
        dy += self.velY

        #ensure player stays on screen
        if self.rect.left + dx < 0:

            dx = 0 - self.rect.left

        if self.rect.right + dx > screenWidth:

            dx = screenWidth - self.rect.right

        if self.rect.bottom + dy > screenHeight - 110:

            self.velY = 0
            self.jump = False
            dy = screenHeight - 110 - self.rect.bottom

        #ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #update player position
        self.rect.x += dx
        self.rect.y += dy

    #handle animation updates
    def update(self):
        
        #check what action the player is performing

        if self.attacking == True:
            if self.attackType == 1:
                self.updateAction(3) #3: attack1
            elif self.attackType == 2:
                self.updateAction(4) #4: attack2
        
        elif self.jump == True:
            self.updateAction(2) #2: jump

        elif self.running == True:
            self.updateAction(1) #1: run

        else:
            self.updateAction(0) #0: idle


        animationCooldown = 50

        #update image
        self.image = self.animationList[self.action][self.frameIndex]

        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.frameIndex += 1
            self.updateTime = pygame.time.get_ticks()

        #check if the animation has finished
        if self.frameIndex >= len(self.animationList[self.action]):
            self.frameIndex = 0

    def attack(self, surface, target):

        self.attacking = True

        attackingRect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)

        if attackingRect.colliderect(target.rect):
            target.health -= 10
            print("Hit")
            print(target.health)



        pygame.draw.rect(surface, (0, 255, 0), attackingRect)


    def updateAction(self, newAction):
        #check if the new action is different to the previous one
        if newAction != self.action:
            self.action = newAction

            #update the animation settings
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()


    def draw(self, surface):

        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.imageScale), self.rect.y - (self.offset[1] * self.imageScale)))
