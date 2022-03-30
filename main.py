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

add_small_enemies(small_enemies, all_enemies, 10)
add_middle_enemies(middle_enemies, all_enemies, 5)
add_big_enemies(big_enemies, all_enemies, 3)

# Collision Checking
myplane_destroy_index = 0
small_enemy_destroy_index = 0
middle_enemy_destroy_index = 0
big_enemy_destroy_index = 0


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

    # Monitoring if myplane is collided with enemy
    collide_list = pygame.sprite.spritecollide(myplane, all_enemies, False, pygame.sprite.collide_mask)
    if collide_list:
        #myplane.active = False
        for each in collide_list:
            each.active = False

    # draw big enemies
    for each in big_enemies:
        # enemy is active
        if each.active:
            each.move()
            if each.rect.bottom == -5:
                enemy3_flying_sound.play(-1)

            if switch_picture:
                screen.blit(each.image1, each.rect)
            else:
                screen.blit(each.image2, each.rect)
        else:
            # enemy become inactive(destroyed)
            enemy3_down_sound.play()
            if not (counter % 3):
                # stop the fly sound and start destroy sound
                if big_enemy_destroy_index == 0:
                    enemy3_flying_sound.stop()

                screen.blit(each.destroy_images[big_enemy_destroy_index], each.rect)
                big_enemy_destroy_index = (big_enemy_destroy_index + 1) % 6
                print('index:', big_enemy_destroy_index)
                if big_enemy_destroy_index == 0:
                    each.reset()

    # draw middle enemies
    for each in middle_enemies:
        if each.active:
            each.move()
            screen.blit(each.image, each.rect)
        else:
            enemy2_down_sound.play()
            if not (counter % 3):
                screen.blit(each.destroy_images[middle_enemy_destroy_index], each.rect)
                middle_enemy_destroy_index = (middle_enemy_destroy_index + 1) % 4
                if middle_enemy_destroy_index % 4 == 0:
                    each.reset()

    # draw small enemies
    for each in small_enemies:
        if each.active:
            each.move()
            screen.blit(each.image, each.rect)
        else:
            enemy1_down_sound.play()
            if not (counter % 3):
                screen.blit(each.destroy_images[small_enemy_destroy_index], each.rect)
                small_enemy_destroy_index = (small_enemy_destroy_index + 1) % 4
                print(small_enemy_destroy_index)
                if small_enemy_destroy_index % 4 == 0:
                    each.reset()

    # draw myplane with different pictures depends on flag
    if myplane.active:
        if switch_picture:
            screen.blit(myplane.image1, myplane.rect)
        else:
            screen.blit(myplane.image2, myplane.rect)
    else:
        me_down_sound.play()
        if not (counter % 3):
            if not (counter % 3):
                screen.blit(myplane.destroy_images[myplane_destroy_index], myplane.rect)
                myplane_destroy_index = (myplane_destroy_index + 1) % 4
                if myplane_destroy_index % 4 == 0:
                    running = False
                    print('GAME OVER!!')

    pygame.display.flip()
    clock.tick(60)

