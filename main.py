import pygame
import sys
import myplane
import enemies
import bullet1
import traceback
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Aircraft Wars")
background = pygame.image.load("images/background.png").convert()
myplane_image1 = "images/me1.png"
myplane_image2 = "images/me2.png"
enemy1_image = "images/enemy1.png"
enemy2_image = "images/enemy2.png"
enemy3_image1 = "images/enemy3_n1.png"
enemy3_image2 = "images/enemy3_n2.png"
pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
bomb_image = pygame.image.load('images/bomb.png').convert_alpha()


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

# bomb setting
bomb_rect = bomb_image.get_rect()
bomb_rect.left, bomb_rect.top = (10, height - bomb_rect.height - 10)
bomb_num = 3
bomb_font = pygame.font.Font('font/font.ttf', 48)

# color for the energy
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Scores Board
scores = 0
scores_font = pygame.font.Font('font/font.ttf', 36)

# Game Pause and Resume flag
paused = False
# get the rect of pause/resume icon and put it into up right corner
pause_rect = pause_nor_image.get_rect()
pause_rect.left, pause_rect.top = (width - pause_rect.width - 10, 10)
pause_image = pause_nor_image

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

def increase_speed(target, num):
    for each in target:
        each.speed += num

add_small_enemies(small_enemies, all_enemies, 10)
add_middle_enemies(middle_enemies, all_enemies, 5)
add_big_enemies(big_enemies, all_enemies, 3)

# index for Collision Checking
myplane_destroy_index = 0
small_enemy_destroy_index = 0
middle_enemy_destroy_index = 0
big_enemy_destroy_index = 0

# bullet initialization
bullets = []
bullet_index = 0
BULLET_NUM = 4
for i in range(BULLET_NUM):
    bullets.append(bullet1.Bullet1(myplane.rect.midtop))

# level for difficulties
level = 1

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # check if the mouse left key pressed and if it is in the icon border
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1 and pause_rect.collidepoint(event.pos):
                paused = not paused
        # when mouse pointer goes into the border of icon it changed to a deeper icon
        elif event.type == MOUSEMOTION:
            if pause_rect.collidepoint(event.pos):
                if paused:
                    pause_image = resume_pressed_image
                else:
                    pause_image = pause_pressed_image
            else:
                if paused:
                    pause_image = resume_nor_image
                else:
                    pause_image = pause_nor_image

        # use space key to use bomb
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if bomb_num:
                    bomb_num -= 1
                    use_bomb_sound.play()
                    # destroy all enemies in the screen
                    for e in all_enemies:
                        if e.rect.bottom > 0:
                            e.active = False

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

    # Monitoring if myplane is collided with enemy
    collide_list = pygame.sprite.spritecollide(myplane, all_enemies, False, pygame.sprite.collide_mask)
    if collide_list:
        #myplane.active = False
        for each in collide_list:
            each.active = False
    # Starting drawing the screen
    screen.blit(background, (0, 0))

    # if not paused then we draw everything, otherwise it will stop
    if not paused:
        # change the bullet position to follow myplane every 10 frames
        if not (counter % 10):
            bullets[bullet_index].reset(myplane.rect.midtop)
            bullet_index = (bullet_index + 1) % BULLET_NUM

        # draw the bullet
        for b in bullets:
            if b.active:
                b.move()
                screen.blit(b.image, b.rect)
                enemy_hit = pygame.sprite.spritecollide(b, all_enemies, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        if e in middle_enemies or e in big_enemies:
                            e.hit = True
                            e.energy -= 1
                            if e.energy == 0:
                                e.active = False
                        else:
                            e.active = False

        # draw big enemies
        for each in big_enemies:
            # enemy is active
            if each.active:
                each.move()
                # draw the energy line of full blood
                pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5),\
                                 (each.rect.right, each.rect.top - 5), 2)
                big_enemy_energy_remain = each.energy / enemies.BigEnemy.energy
                # if the energy lower than 20%, draw red line, otherwise draw green line
                if big_enemy_energy_remain > 0.2:
                    color = GREEN
                else:
                    color = RED
                pygame.draw.line(screen, color, (each.rect.left, each.rect.top - 5),\
                                 (each.rect.left + each.rect.width * big_enemy_energy_remain, each.rect.top - 5), 2)

                if each.rect.bottom == -5:
                    enemy3_flying_sound.play(-1)
                # draw the enemy hit picture
                if each.hit:
                    screen.blit(each.image_hit, each.rect)
                    each.hit = False
                else:
                    if switch_picture:
                        screen.blit(each.image1, each.rect)
                    else:
                        screen.blit(each.image2, each.rect)
            else:
                # enemy become inactive(destroyed)
                if not (counter % 3):
                    # start destroy sound
                    if big_enemy_destroy_index == 0:
                        enemy3_down_sound.play()

                    screen.blit(each.destroy_images[big_enemy_destroy_index], each.rect)
                    big_enemy_destroy_index = (big_enemy_destroy_index + 1) % 6

                    if big_enemy_destroy_index == 0:
                        # stop the fly sound
                        enemy3_flying_sound.stop()
                        scores += 10000
                        each.reset()

        # draw middle enemies
        for each in middle_enemies:
            if each.active:
                each.move()
                # draw the energy line of full blood
                pygame.draw.line(screen, BLACK, (each.rect.left, each.rect.top - 5), \
                                 (each.rect.right, each.rect.top - 5), 2)
                middle_enemy_energy_remain = each.energy / enemies.MiddleEnemy.energy
                # if the energy lower than 20%, draw red line, otherwise draw green line
                if middle_enemy_energy_remain > 0.2:
                    color = GREEN
                else:
                    color = RED
                pygame.draw.line(screen, color, (each.rect.left, each.rect.top - 5), \
                                 (each.rect.left + each.rect.width * middle_enemy_energy_remain, each.rect.top - 5), 2)

                # draw the enemy hit picture
                if each.hit:
                    screen.blit(each.image_hit, each.rect)
                    each.hit = False
                else:
                    screen.blit(each.image, each.rect)
            else:
                # middle enemy down
                if not (counter % 3):
                    if middle_enemy_destroy_index == 0:
                        enemy2_down_sound.play()
                    screen.blit(each.destroy_images[middle_enemy_destroy_index], each.rect)
                    middle_enemy_destroy_index = (middle_enemy_destroy_index + 1) % 4
                    if middle_enemy_destroy_index % 4 == 0:
                        scores += 6000
                        each.reset()

        # draw small enemies
        for each in small_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)
            else:
                # small enemy down
                if not (counter % 3):
                    if small_enemy_destroy_index == 0:
                        enemy1_down_sound.play()
                    screen.blit(each.destroy_images[small_enemy_destroy_index], each.rect)
                    small_enemy_destroy_index = (small_enemy_destroy_index + 1) % 4
                    if small_enemy_destroy_index % 4 == 0:
                        scores += 1000
                        each.reset()

        # draw myplane with different pictures depends on flag
        if myplane.active:
            if switch_picture:
                screen.blit(myplane.image1, myplane.rect)
            else:
                screen.blit(myplane.image2, myplane.rect)
        else:
            # myplane was down
            if not (counter % 3):
                if myplane_destroy_index == 0:
                    me_down_sound.play()
                screen.blit(myplane.destroy_images[myplane_destroy_index], myplane.rect)
                myplane_destroy_index = (myplane_destroy_index + 1) % 4
                if myplane_destroy_index % 4 == 0:
                    pygame.time.delay(500)
                    running = False
                    print('GAME OVER!!')

        # draw the bomb
        bomb_text = bomb_font.render(('x %s' % str(bomb_num)), True, WHITE)
        screen.blit(bomb_image, bomb_rect)
        screen.blit(bomb_text, (bomb_rect.width + 20, bomb_rect.top))

    # draw the scores board
    scores_text = scores_font.render(('Scores: %s' % str(scores)), True, WHITE)
    scores_rect = scores_text.get_rect()
    scores_rect.left, scores_rect.top = 10, 5
    screen.blit(scores_text, scores_rect)

    # draw the Pause/Resume Icon
    screen.blit(pause_image, pause_rect)



    # difficult level changing
    # level 2, add small 3, middle 2, big 1, small speed+1
    if level == 1 and scores > 50000:
        level = 2
        upgrade_sound.play()
        add_small_enemies(small_enemies, all_enemies, 3)
        add_middle_enemies(middle_enemies, all_enemies, 2)
        add_big_enemies(big_enemies, all_enemies, 1)
        increase_speed(small_enemies, 1)
    # level 3, add small 5, middle 3, big 2, small speed+1, middle speed + 1
    elif level == 2 and scores > 300000:
        level == 3
        upgrade_sound.play()
        add_small_enemies(small_enemies, all_enemies, 5)
        add_middle_enemies(middle_enemies, all_enemies, 3)
        add_big_enemies(big_enemies, all_enemies, 2)
        increase_speed(small_enemies, 1)
        increase_speed(middle_enemies, 1)
    # level 4
    elif level == 3 and scores > 600000:
        level == 4
        upgrade_sound.play()
        add_small_enemies(small_enemies, all_enemies, 5)
        add_middle_enemies(middle_enemies, all_enemies, 3)
        add_big_enemies(big_enemies, all_enemies, 2)
        increase_speed(small_enemies, 1)
        increase_speed(middle_enemies, 1)
    # level 5
    elif level == 4 and scores > 1000000:
        level == 5
        upgrade_sound.play()
        add_small_enemies(small_enemies, all_enemies, 5)
        add_middle_enemies(middle_enemies, all_enemies, 3)
        add_big_enemies(big_enemies, all_enemies, 2)
        increase_speed(small_enemies, 1)
        increase_speed(middle_enemies, 1)

    pygame.display.flip()
    clock.tick(60)

