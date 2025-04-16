import pygame

class Projectile:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y, 20, 10)
        self.speed = 12 * direction

    def update(self):
        self.rect.x += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 255), self.rect)
