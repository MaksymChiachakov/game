import pygame 
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT, K_s, K_w, K_d, K_a
import sys
import os
import sqlite3
# Отримайте поточний шлях
current_dir = os.path.dirname(os.path.abspath(__file__))

# Додайте шлях до батьківської директорії до шляхів Python
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)

# Тепер ви можете імпортувати модуль
#from db import request_for_DB # Замість "module" тут повинна бути назва вашого модулю
from db import get_catch, delete_catch_score


pygame.init()

pygame.display.set_caption('Доганялки')
FPS = pygame.time.Clock()
w, h = 1200, 800

FONT = pygame.font.SysFont('Verdana', 20)

color_black = (0, 0, 0)

main_display = pygame.display.set_mode((w, h))

def get_score(score):
    return score

def push_to_db():
    first = []
    first.append(score)
    data = first.copy()

    int_element = data[0]

    conn = sqlite3.connect('DB.db')

        # cursor - працює з запитами у DB
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO catch (score) VALUES (?)''', [int_element])

    conn.commit()

bg = pygame.transform.scale(pygame.image.load('img/for catch/background.png'), (w, h))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

pl1 = pygame.transform.scale(pygame.image.load('img/for catch/catch2.png'), (80, 80))
pl1_rect = pl1.get_rect()
pl1_move_down = [0, 4]
pl1_move_up = [0, -4]
pl1_speed_left = [-4, 0]
pl1_speed_right = [4, 0]

pl2 = pygame.transform.scale(pygame.image.load('img/for catch/catch1.png'), (80,80))
pl2_rect = pl2.get_rect(center=(w/2, h/2))
pl2_move_down = [0, 3]
pl2_move_up = [0, -3]
pl2_speed_left = [-3, 0]
pl2_speed_right = [3, 0]

CHANGE_IMAGE = pygame.USEREVENT + 1
pygame.time.set_timer(CHANGE_IMAGE, 200)

score = 0 

playing = True
while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            push_to_db()
            get_catch()
            delete_catch_score()
            #restart_data()
            playing = False
            


    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and pl1_rect.bottom < h:
        pl1_rect = pl1_rect.move(pl1_move_down)

    if keys[K_UP] and pl1_rect.top >= 0:
        pl1_rect = pl1_rect.move(pl1_move_up)

    if keys[K_RIGHT] and pl1_rect.right < w:
        pl1_rect = pl1_rect.move(pl1_speed_right)

    if keys[K_LEFT] and pl1_rect.left >= 0:
        pl1_rect = pl1_rect.move(pl1_speed_left)

    if keys[K_s] and pl2_rect.bottom < h:
        pl2_rect = pl2_rect.move(pl2_move_down)

    if keys[K_w] and pl2_rect.top >= 0:
        pl2_rect = pl2_rect.move(pl2_move_up)

    if keys[K_d] and pl2_rect.right < w:
        pl2_rect = pl2_rect.move(pl2_speed_right)

    if keys[K_a] and pl2_rect.left >= 0:
        pl2_rect = pl2_rect.move(pl2_speed_left)

    if pl1_rect.colliderect(pl2_rect) and not collision_detected:
        score += 1
        collision_detected = True  # Позначаємо зіткнення, щоб не додавати більше очок


    if not pl1_rect.colliderect(pl2_rect):
        collision_detected = False  # Скидаємо позначку при відсутності зіткнення

    if score == 10:
        push_to_db()
        get_catch()
        #restart_data()
        delete_catch_score()
        playing = False
        




    main_display.blit(FONT.render(str(score), True, color_black), (w-70, 20))
    main_display.blit(pl1, pl1_rect)
    main_display.blit(pl2, pl2_rect)

    pygame.display.flip()

#i = 0
#while i == 1:
    #if playing == False:
        #get_maze()
        #i += 1

# Надсилання очок у DB
