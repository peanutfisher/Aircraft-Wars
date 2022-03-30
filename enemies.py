import pygame
import random

pygame.init()

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self, image, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert_alpha()
        self.destroy_images = [pygame.image.load('images\enemy1_down1.png').convert_alpha(), pygame.image.load('images\enemy1_down2.png').convert_alpha(),\
                               pygame.image.load('images\enemy1_down3.png').convert_alpha(), pygame.image.load('images\enemy1_down4.png').convert_alpha()]
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-3 * self.height, 0)
        self.speed = 3
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                          random.randint(-3 * self.height, 0)

class MiddleEnemy(pygame.sprite.Sprite):
    def __init__(self, image, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image).convert_alpha()
        self.destroy_images = [pygame.image.load('images\enemy2_down1.png').convert_alpha(), pygame.image.load('images\enemy2_down2.png').convert_alpha(),\
                               pygame.image.load('images\enemy2_down3.png').convert_alpha(), pygame.image.load('images\enemy2_down4.png').convert_alpha()]
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-6 * self.height, -3 * self.height)
        self.speed = 2
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                          random.randint(-6 * self.height, -3 * self.height)

class BigEnemy(pygame.sprite.Sprite):
    def __init__(self, image1, image2, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load(image1).convert_alpha()
        self.image2 = pygame.image.load(image2).convert_alpha()
        self.destroy_images = [pygame.image.load('images\enemy3_down1.png').convert_alpha(), pygame.image.load('images\enemy3_down2.png').convert_alpha(),\
                               pygame.image.load('images\enemy3_down3.png').convert_alpha(), pygame.image.load('images\enemy3_down4.png').convert_alpha(),\
                               pygame.image.load('images\enemy3_down5.png').convert_alpha(), pygame.image.load('images\enemy3_down6.png').convert_alpha()]
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                        random.randint(-9 * self.height, -6 * self.height)
        self.speed = 1
        self.active = True
        self.mask = pygame.mask.from_surface(self.image1)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = random.randint(0, self.width - self.rect.width), \
                                          random.randint(-9 * self.height, -6 * self.height)