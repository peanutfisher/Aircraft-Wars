import pygame
import random

pygame.init()

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, image, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-5 * self.height, 0)
        self.speed = 3

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                          random.randint(-5 * self.height, 0)

class MiddleEnemy(pygame.sprite.Sprite):
    def __init__(self, image, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-10 * self.height, -5 * self.height)
        self.speed = 2

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                          random.randint(-10 * self.height, -5 * self.height)

class BigEnemy(pygame.sprite.Sprite):
    def __init__(self, image1, image2, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load(image1).convert_alpha()
        self.image2 = pygame.image.load(image2).convert_alpha()
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-15 * self.height, -10 * self.height)
        self.speed = 1

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                          random.randint(-15 * self.height, -10 * self.height)