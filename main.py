import pygame
import sys
import plane
import enemies
import bullet
import supply

import traceback
from pygame.locals import *
from random import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Aircraft Wars")
background = pygame.image.load("images/background.png").convert()
clock = pygame.time.Clock()

pause_nor_image = pygame.image.load('images/pause_nor.png').convert_alpha()
pause_pressed_image = pygame.image.load('images/pause_pressed.png').convert_alpha()
resume_nor_image = pygame.image.load('images/resume_nor.png').convert_alpha()
resume_pressed_image = pygame.image.load('images/resume_pressed.png').convert_alpha()
bomb_image = pygame.image.load('images/bomb.png').convert_alpha()
restart_image = pygame.image.load('images/again.png').convert_alpha()
gameover_image = pygame.image.load('images/gameover.png').convert_alpha()

# methods to add small/middle/big enemies into their group and also put them together for collision check
def add_small_enemies(group1, group2, num):
    for i in range(num):
        smallenemy = enemies.SmallEnemy(bg_size)
        group1.add(smallenemy)
        group2.add(smallenemy)

def add_middle_enemies(group1, group2, num):
    for i in range(num):
        middleenemy = enemies.MiddleEnemy(bg_size)
        group1.add(middleenemy)
        group2.add(middleenemy)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        bigenemy = enemies.BigEnemy(bg_size)
        group1.add(bigenemy)
        group2.add(bigenemy)

def increase_speed(target, num):
    for each in target:
        each.speed += num


# background music and Sounds
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
enemy3_flying_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_flying_sound.set_volume(0.5)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
use_bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
use_bomb_sound.set_volume(0.2)


def main():
    # create myplane
    myplane = plane.MyPlane(bg_size)

    # flag for game running
    running = True

    # lives of myplane
    life_num = 3
    life_image = pygame.image.load('images/life.png').convert_alpha()
    life_rect = life_image.get_rect()

    # bomb setting
    bomb_rect = bomb_image.get_rect()
    bomb_rect.left, bomb_rect.top = (10, height - bomb_rect.height - 10)
    bomb_num = 3
    bomb_font = pygame.font.Font('font/font.ttf', 48)

    # Scores Board
    scores = 0
    scores_font = pygame.font.Font('font/font.ttf', 36)

    # Game Pause and Resume flag
    paused = False
    # get the rect of pause/resume icon and put it into up right corner
    pause_rect = pause_nor_image.get_rect()
    pause_rect.left, pause_rect.top = (width - pause_rect.width - 10, 10)
    pause_image = pause_nor_image

    # images setting for game over scene
    restart_rect = restart_image.get_rect()
    restart_rect.left, restart_rect.top = (width - restart_rect.width) // 2, height * 2 / 3

    gameover_rect = restart_image.get_rect()
    gameover_rect.left, gameover_rect.top = (width - gameover_rect.width) // 2, height * 2 / 3 + 45
    gameover_font = pygame.font.Font('font/font.ttf', 45)

    # color for the energy
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

    # storing key_pressed value
    key_pressed_list = []

    # the flag of switching pictures
    switch_picture = False

    # a kind of timer(delay)
    counter = 120

    # groups of enemies
    all_enemies = pygame.sprite.Group()
    small_enemies = pygame.sprite.Group()
    middle_enemies = pygame.sprite.Group()
    big_enemies = pygame.sprite.Group()

    # added enemies
    add_small_enemies(small_enemies, all_enemies, 10)
    add_middle_enemies(middle_enemies, all_enemies, 5)
    add_big_enemies(big_enemies, all_enemies, 3)

    # index for Collision Checking
    myplane_destroy_index = 0
    small_enemy_destroy_index = 0
    middle_enemy_destroy_index = 0
    big_enemy_destroy_index = 0

    # normal bullet(bullet1) initialization
    bullets = []
    bullets1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullets1.append(bullet.Bullet1(myplane.rect.midtop))

    # super bullet(bullet2) initialization
    super_bullet_flag = False
    bullets2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM // 2):
        bullets2.append(bullet.Bullet2((myplane.rect.centerx - 33, myplane.rect.centery)))
        bullets2.append(bullet.Bullet2((myplane.rect.centerx + 30, myplane.rect.centery)))

    # level for difficulties
    level = 1

    # TIMER for providing supply every 30s
    SUPPLY_TIMER  = USEREVENT
    pygame.time.set_timer(SUPPLY_TIMER, 30 * 1000)

    # TIMER for super bullet(last 18s)
    BULLET2_TIMER = USEREVENT + 1

    # TIMER for myplane invincible time(3s)
    INVINCIBLE_TIMER = USEREVENT + 2

    # initialize the supply
    bullet_supply = supply.Bullet_supply(bg_size)
    bomb_supply = supply.Bomb_supply(bg_size)
    current_supply = bullet_supply

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # check if the mouse left key pressed and if it is in the icon border
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    paused = not paused
                    # if paused the game then background music and sounds all are paused.
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIMER, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIMER, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

                # click the image to restart the game
                elif event.button == 1 and restart_rect.collidepoint(event.pos):
                    main()
                # click the image to quit the game
                elif event.button == 1 and gameover_rect.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                    sys.exit()

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

            # provide the supply after get a USEREVENT every 30s
            elif event.type == SUPPLY_TIMER:
                supply_sound.play()
                if choice([True, False]):
                    bullet_supply.reset()
                else:
                    bomb_supply.reset()

            # Timer for super bullet(18s)
            elif event.type == BULLET2_TIMER:
                super_bullet_flag = False

            # Timer for myplane invincible after born again
            elif event.type == INVINCIBLE_TIMER:
                myplane.invincible = False

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
        if collide_list and not myplane.invincible:
            myplane.active = False
            for each in collide_list:
                each.active = False

        # Starting drawing the screen
        screen.blit(background, (0, 0))

        # if not paused then we draw everything, otherwise it will stop
        if not paused and life_num:
            # change the bullet position to follow myplane every 10 frames
            if not (counter % 10):
                # change the bullet rect to follow with myplane
                bullets1[bullet1_index].reset(myplane.rect.midtop)
                bullet1_index = (bullet1_index + 1) % BULLET1_NUM

                # odd bullet in the left gun, even bullet in the right gun
                bullets2[bullet2_index].reset((myplane.rect.centerx - 33, myplane.rect.centery))
                bullets2[bullet2_index + 1].reset((myplane.rect.centerx + 30, myplane.rect.centery))
                bullet2_index = (bullet2_index + 2) % BULLET2_NUM

            # check if super bullet got
            if super_bullet_flag:
                bullets = bullets2
            else:
                bullets = bullets1

            # draw the bullet
            for b in bullets:
                if b.active:
                    bullet_sound.play()
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
                        life_num -= 1
                        myplane.reset()
                        pygame.time.set_timer(INVINCIBLE_TIMER, 3 * 1000)

            # draw the life picture of myplane
            for i in range(1, (life_num + 1)):
                life_rect.left, life_rect.top = width - life_rect.width * i - 10, height - life_rect.height - 10
                screen.blit(life_image, life_rect)

            # draw the bomb
            bomb_text = bomb_font.render(('x %s' % str(bomb_num)), True, WHITE)
            screen.blit(bomb_image, bomb_rect)
            screen.blit(bomb_text, (bomb_rect.width + 20, bomb_rect.top))

            # draw the bullet supply and bomb supply
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, myplane):
                    get_bullet_sound.play()
                    super_bullet_flag = True
                    print('super bullet flag', super_bullet_flag)
                    pygame.time.set_timer(BULLET2_TIMER, 18 * 1000)
                    bullet_supply.active = False

            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, myplane):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            # draw the scores board
            scores_text = scores_font.render(('Scores: %s' % str(scores)), True, WHITE)
            scores_rect = scores_text.get_rect()
            scores_rect.left, scores_rect.top = 10, 5
            screen.blit(scores_text, scores_rect)

            # draw the Pause/Resume Icon
            screen.blit(pause_image, pause_rect)

            # difficulty level setting
            # level 2, add small 3, middle 2, big 1, small speed+1
            if level == 1 and scores > 500000:
                level = 2
                upgrade_sound.play()
                add_small_enemies(small_enemies, all_enemies, 3)
                add_middle_enemies(middle_enemies, all_enemies, 2)
                add_big_enemies(big_enemies, all_enemies, 1)
                increase_speed(small_enemies, 1)
            # level 3, add small 5, middle 3, big 2, small speed+1, middle speed + 1
            elif level == 2 and scores > 1000000:
                level == 3
                upgrade_sound.play()
                add_small_enemies(small_enemies, all_enemies, 5)
                add_middle_enemies(middle_enemies, all_enemies, 3)
                add_big_enemies(big_enemies, all_enemies, 2)
                increase_speed(small_enemies, 1)
                increase_speed(middle_enemies, 1)
            # level 4
            elif level == 3 and scores > 1500000:
                level == 4
                upgrade_sound.play()
                add_small_enemies(small_enemies, all_enemies, 5)
                add_middle_enemies(middle_enemies, all_enemies, 3)
                add_big_enemies(big_enemies, all_enemies, 2)
                increase_speed(small_enemies, 1)
                increase_speed(middle_enemies, 1)
            # level 5
            elif level == 4 and scores > 2000000:
                level == 5
                upgrade_sound.play()
                add_small_enemies(small_enemies, all_enemies, 5)
                add_middle_enemies(middle_enemies, all_enemies, 3)
                add_big_enemies(big_enemies, all_enemies, 2)
                increase_speed(small_enemies, 1)
                increase_speed(middle_enemies, 1)

        # Game over when all myplane lives gone
        elif not life_num:
            # stop the music, sound and supply timer
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer(SUPPLY_TIMER, 0)

            # read the highest scores from history
            with open('records.txt', 'r') as f:
                highest_scores = f.read()
                if highest_scores == '':
                    highest_scores = 0

            # compare your scores with historical highest scores and note the new highest
            if scores > int(highest_scores):
                with open('records.txt', 'w') as f:
                    f.write(str(scores))

            # draw the highest scores / Your scores / restart / game over pictures
            highest_scores_text = scores_font.render(('Highest Scores: %s' % highest_scores), True, WHITE)
            highest_scores_rect = highest_scores_text.get_rect()
            highest_scores_rect.left, highest_scores_rect.top = 30, 50

            your_scores_text = gameover_font.render(('Your Scores: %s' % str(scores)), True, WHITE)
            your_scores_rect = your_scores_text.get_rect()
            your_scores_rect.center = width // 2, height / 3

            screen.blit(highest_scores_text, highest_scores_rect)
            screen.blit(your_scores_text, your_scores_rect)
            screen.blit(restart_image, restart_rect)
            screen.blit(gameover_image, gameover_rect)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
