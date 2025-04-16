import pygame

from projectiles import Projectile

class Fighter():
    
    def __init__(self, x, y):

        self.flip = False
        self.rect = pygame.Rect((x, y, 80, 180))

        #Y velocity
        self.velY = 0
        self.jump = False
        self.attacking = False
       

        #which attack is being used
        self.attackType = 0

        self.health = 100

    def move(self, screenWidth, screenHeight, surface, target):

        speed = 10
        gravity = 2
        dx = 0
        dy = 0

        #get keypresses
        key = pygame.key.get_pressed()

        #can only perform other actions if not currently attacking
        if self.attacking == False:

            #movement
            if key[pygame.K_a]:
                dx = -speed
                self.facingLeft = True

            if key[pygame.K_d]:
                dx = speed
                self.facingLeft = False
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

    def attack(self, surface, target):

        self.attacking = True

        attackingRect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)

        if attackingRect.colliderect(target.rect):
            target.health -= 10
            print("Hit")
            print(target.health)



        pygame.draw.rect(surface, (0, 255, 0), attackingRect)




    def draw(self, surface):

        pygame.draw.rect(surface, (255, 0, 0), self.rect)
