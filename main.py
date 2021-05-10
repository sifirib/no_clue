import pygame
from pygame import mixer
import os
import math
from Background import *
from Screen import *
from Button import *
from Character import *
from SpaceShip import *
from Planet import *
from shared import *


# Initialize the pygame
pygame.init()

# Create the screen
main_menu = Menu("main", [1024, 850], "space.png", "background_music.wav", "MOOM", "icon")
main_menu.background.set_tiles([[main_menu.background_image]])

# Load media for screen
main_menu.load("music")
animated_moon = pygame.image.load(os.path.join("images", "moon.png")).convert_alpha()

# Display the screen
main_menu.set_("screen")
main_menu.set_("caption")

# Background music
# mixer.music.play(-1)

# Buttonschar1.hitbox = (char1.x + 20, char1.y, 15, 60)
play_button = Button((0, 100, 0), 20, 300, 120, 80, 'Play')
settings_button = Button((0, 100, 0), 20, 350, 120, 80, 'Options')
leave_button = Button((0, 100, 0), 20, 400, 120, 80, 'Leave')

#Planet
earth = Planet()

# Character
char = Character("girl", [350, 400], main_menu, earth)
char.jump_step = char.jump_power = 10

char1 = Character("boy", [400, 400], main_menu, earth)
char1.run_speed = char1.walk_speed + 6
char1.jump_step = char1.jump_power = 12
char1.controllers = {"jump": pygame.K_w,
                     "right": pygame.K_d,
                     "left": pygame.K_a,
                     "run": pygame.K_LSHIFT}

ship = SpaceShip("4_Red.png", char, main_menu, [300, 300])
ship1 = SpaceShip("4_Red.png", char1, main_menu, [300, 400])
ship1.controllers["crouch"] = pygame.K_s

def redraw_game_screen(*args, window):
    objects = args

    window.screen.blit(animated_moon, (moon_width, moon_height))
    ship.draw()
    ship1.draw()
    for obj in objects:
        obj.draw(window.screen)

    play_button.draw(window.screen)
    settings_button.draw(window.screen)
    leave_button.draw(window.screen)
    pygame.display.update()


# Clock
clock =  pygame.time.Clock()
fps = 45

# Game loop
main_menu_loop = True
moon_loop = 0
moon_width = -300
moon_height = -200
play_loop = False

while main_menu_loop:
    # print(int(pygame.time.Clock().get_fps()))
    clock.tick(fps)

    moon_loop += 1
    if moon_loop == 5:
        moon_loop = 1
        moon_width += 10
        moon_height += 5

        if moon_width == 4000:
            moon_width = -300
            moon_height = -200

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            main_menu_loop = False
            pygame.quit()
            quit()

        # MOUSE behaviours
        if event.type == pygame.MOUSEBUTTONDOWN:
            if leave_button.is_over(pos):
                main_menu_loop = False
                pygame.quit()
                quit()
            if play_button.is_over(pos):
                play_loop = True

        if event.type == pygame.MOUSEMOTION:
            if play_button.is_over(pos):
                play_button.font_size = 20
            else:
                play_button.font_size = 16
            if leave_button.is_over(pos):
                leave_button.font_size = 20
            else:
                leave_button.font_size = 16
            if settings_button.is_over(pos):
                settings_button.font_size = 20
            else:
                settings_button.font_size = 16

    # KEYBOARD behaviours
    # char.keyboard_behaviours()
    # char1.keyboard_behaviours()
    # char.action()
    # char1.action()
    ship.keyboard_behaviours()
    ship1.keyboard_behaviours()
    ship.action()
    ship1.action()

    if is_collision(char.collision, char1.collision):
        pass
    redraw_game_screen(char, char1, window=main_menu)

    while play_loop:
        print("Crash crash crash C:")
