import pygame
import sys
import myplane
import enemies
import traceback
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Aircraft Wars")
background = pygame.image.load("images\\background.png").convert()
myplane_image1 = "images\\me1.png"
myplane_image2 = "images\\me2.png"
enemy1_image = "images\\enemy1.png"
enemy2_image = "images\\enemy2.png"
enemy3_image1 = "images\\enemy3_n1.png"
enemy3_image2 = "images\\enemy3_n2.png"

clock = pygame.time.Clock()

running = True

# background music and Sounds
pygame.mixer.music.load("sound\\game_music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
bullet_sound = pygame.mixer.Sound("sound\\bullet.wav")
bullet_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound\\enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound\\enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound\\enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
enemy3_flying_sound = pygame.mixer.Sound("sound\\enemy3_flying.wav")
enemy3_flying_sound.set_volume(0.5)
get_bomb_sound = pygame.mixer.Sound("sound\\get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound\\get_bullet.wav")
get_bullet_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound\\me_down.wav")
me_down_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound\\supply.wav")
supply_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound\\upgrade.wav")
upgrade_sound.set_volume(0.2)
use_bomb_sound = pygame.mixer.Sound("sound\\use_bomb.wav")
use_bomb_sound.set_volume(0.2)

# create myplane
myplane = myplane.MyPlane(myplane_image1, myplane_image2, bg_size)


# groups of enemies
all_enemies = pygame.sprite.Group()
small_enemies = pygame.sprite.Group()
middle_enemies = pygame.sprite.Group()
big_enemies = pygame.sprite.Group()

# storing key_pressed value
key_pressed_list = []
# the flag of switching pictures
switch_picture = False
# a kind of timer
counter = 120

# methods to add small/middle/big enemies into their group and also put them together for collision check
def add_small_enemies(group1, group2, num):
    for i in range(num):
        smallenemy = enemies.SmallEnemy(enemy1_image, bg_size)
        group1.add(smallenemy)
        group2.add(smallenemy)

def add_middle_enemies(group1, group2, num):
    for i in range(num):
        middleenemy = enemies.MiddleEnemy(enemy2_image, bg_size)
        group1.add(middleenemy)
        group2.add(middleenemy)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        bigenemy = enemies.BigEnemy(enemy3_image1, enemy3_image2, bg_size)
        group1.add(bigenemy)
        group2.add(bigenemy)

add_small_enemies(small_enemies, all_enemies, 15)
add_middle_enemies(middle_enemies, all_enemies, 7)
add_big_enemies(big_enemies, all_enemies, 3)

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # get the key_pressed list(boolean)
    key_pressed_list = pygame.key.get_pressed()
    # Use WSAD or UP/DOWN/LEFT/RIGHT to move myplane
    if key_pressed_list[K_w] or key_pressed_list[K_UP]:
        myplane.moveUp()

    if key_pressed_list[K_s] or key_pressed_list[K_DOWN]:
        myplane.moveDown()

    if key_pressed_list[K_a] or key_pressed_list[K_LEFT]:
        myplane.moveLeft()

    if key_pressed_list[K_d] or key_pressed_list[K_RIGHT]:
        myplane.moveRight()

    # every 5 frames we change the flag of switch_picture
    counter -= 1
    if counter % 5 == 0:
        switch_picture = not switch_picture
    if not counter:
        counter = 120

    screen.blit(background, (0,0))
    # draw myplane with different pictures depends on flag
    if switch_picture:
        screen.blit(myplane.image1, myplane.rect)
    else:
        screen.blit(myplane.image2, myplane.rect)

    # draw big enemies
    for each in big_enemies:
        each.move()
        if each.rect.bottom == -5:
            enemy3_flying_sound.play()

        if switch_picture:
            screen.blit(each.image1, each.rect)
        else:
            screen.blit(each.image2, each.rect)

    # draw middle enemies
    for each in middle_enemies:
        each.move()
        screen.blit(each.image, each.rect)

    # draw small enemies
    for each in small_enemies:
        each.move()
        screen.blit(each.image, each.rect)

    pygame.display.flip()
    clock.tick(60)

# git test