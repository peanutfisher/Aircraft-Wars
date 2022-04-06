import pygame
from random import *

pygame.init()

# class for supper bullet supply
class Bullet_supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bullet_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width - 10), -100
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False
        self.speed = 4

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width - 10), -100

# class for bomb supply
class Bomb_supply(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('images/bomb_supply.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width - 10), -100
        self.mask = pygame.mask.from_surface(self.image)
        self.active = False
        self.speed = 4

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False

    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width - 10), -100