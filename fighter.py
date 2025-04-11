import pygame

class Fighter():
    
    def __init__(self, x, y):

        self.rect = pygame.Rect((x, y, 80, 180))

        #Y velocity
        self.velY = 0

    def move(self, screenWidth, screenHeight):

        speed = 10
        gravity = 2
        dx = 0
        dy = 0

        #get keypresses
        key = pygame.key.get_pressed()

        #movement
        if key[pygame.K_a]:
            dx = -speed 
        if key[pygame.K_d]:
            dx = speed
        #jump
        if key[pygame.K_w]:
            self.velY = -30

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
            dy = screenHeight - 110 - self.rect.bottom

        #update player position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, surface):

        pygame.draw.rect(surface, (255, 0, 0), self.rect)
