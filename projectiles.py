import pygame

class Projectile:
    def __init__(self, x, y, radius, color, facing):
        #initialize the projectile w position size color direction and speed
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing  #adjust velocity based on direction projectile is facing
        self.is_active = True  #to determine if projectile's still active
        self.max_distance = 600  #maximum distance projectile can travel
        self.travelled = 0  #keeps track of how far the projectile has traveled

    def move(self):
        #moves the projectile left or right based on direction
        if self.is_active:
            self.x += self.vel  #move based on velocity
            self.travelled += abs(self.vel)  #increase the distance tracker

            #deactivate the projectile if it travels farther than maximum distance
            if self.travelled > self.max_distance:
                self.is_active = False

    def draw(self, win):
        #draws projectile as circle instead of rect
        if self.is_active:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


