import pygame

class Projectile:
    def __init__(self, x, y, radius, color, facing, damage):
        #initialize the projectile with position, size, color, direction, and speed
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing  # adjust velocity based on direction the projectile is facing
        self.is_active = True  # to determine if the projectile's still active
        self.max_distance = 600  # maximum distance projectile can travel
        self.travelled = 0  # keeps track of how far the projectile has traveled
        self.damage = damage  # damage dealt by the projectile

    def move(self):
        #move the projectile left or right based on direction
        if self.is_active:
            self.x += self.vel  # move based on velocity
            self.travelled += abs(self.vel)  # increase the distance tracker

            #deactivate the projectile if it travels farther than the maximum distance
            if self.travelled > self.max_distance:
                self.is_active = False

    def check_collision(self, target):
        #check if the projectile collides with the target
        projectile_rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        if self.is_active and projectile_rect.colliderect(target.rect):  # check if the projectile collides with the target
            target.health -= self.damage  # deal damage to the target
            self.is_active = False  # deactivate the projectile after a hit
            print(f"Hit! Target health: {target.health}")
            return True  # return True if collision happened
        return False

    def draw(self, win):
        #draw the projectile as a circle
        if self.is_active:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
