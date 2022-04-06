import pygame

pygame.init()

# normal bullet shooting from midtop of myplane
class Bullet1(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 12
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

# supper bullet got from bullet supply
class Bullet2(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 12
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True