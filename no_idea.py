import pygame
from pygame import mixer
import os
import math
# from Background import Background 
# from Screen import Screen, Menu
# from Button import Button
# from Character import Character
# from SpaceShip import SpaceShip

class Screen:
    def __init__(self, name, sizes, background_image, background_music, caption, icon):
        self.name = name
        self.x = self.y = 0
        self.width = sizes[0]
        self.height = sizes[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = background_image
        self.background = Background(self.screen)
        self.y2 = self.height  #self.background_image.get_height()
        self.x2 = self.width   #self.background_image.get_width()
        self.background_music = background_music
        self.caption = caption
        self.icon = icon
        
    def load(self, what):
        if what == "music":
            path = os.path.join("sounds", self.background_music)
            if os.path.isfile(path):
                file_ = self.background_music = mixer.music.load(path)
            else:
                raise Exception("Error loading file: " + path + " - Check filename and path?")
        elif what == "image":
            path = os.path.join("images", self.background_image)
            if os.path.isfile(path):
                file_ = self.background_image = pygame.image.load(path).convert_alpha()
            else:
                raise Exception("Error loading file: " + path + " - Check filename and path?")
        
        return file_
    
    def set_(self, what):
        if what == "screen":
            pygame.display.set_mode((self.width, self.height))
        elif what == "caption":
            pygame.display.set_caption(self.caption)
        elif what == "icon":
            pygame.display.set_icon(self.icon)
    
    def fill(self, color):
        self.screen.fill(color)
        
    def blit(self, image, positions):
        self.screen.blit(image, positions)

def load_image(file_name, useColorKey=False):
    path = os.path.join("images", file_name)
    if os.path.isfile(path):
        image = pygame.image.load(path)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception("Error loading image: " + path + " - Check filename and path?")

def parse_colour(colour):
    if type(colour) == str:
        # check to see if valid colour
        return pygame.Color(colour)
    else:
        colourRGB = pygame.Color("white")
        colourRGB.r = colour[0]
        colourRGB.g = colour[1]
        colourRGB.b = colour[2]

        return colourRGB

class Background():
    def __init__(self, screen):
        self.screen = screen
        self.colour = pygame.Color("black")

    def set_tiles(self, tiles):
        if type(tiles) is str:
            self.tiles = [[load_image(tiles)]]
        elif type(tiles[0]) is str:
            self.tiles = [[load_image(i) for i in tiles]]
        else:
            self.tiles = [[load_image(i) for i in row] for row in tiles]
        self.stage_pos_x = 0
        self.stage_pos_y = 0
        self.tile_width = self.tiles[0][0].get_width()
        self.tile_height = self.tiles[0][0].get_height()
        self.screen.blit(self.tiles[0][0], [0, 0])
        self.surface = self.screen.copy()

    def scroll(self, x, y):
        self.stage_pos_x -= x
        self.stage_pos_y -= y
        col = (self.stage_pos_x % (self.tile_width * len(self.tiles[0]))) // self.tile_height
        xOff = (0 - self.stage_pos_x % self.tile_width)
        row = (self.stage_pos_y % (self.tile_height * len(self.tiles))) // self.tile_height
        yOff = (0 - self.stage_pos_y % self.tile_height)

        col2 = ((self.stage_pos_x + self.tile_width) % (self.tile_width * len(self.tiles[0]))) // self.tile_width
        row2 = ((self.stage_pos_y + self.tile_height) % (self.tile_height * len(self.tiles))) // self.tile_height
        self.screen.blit(self.tiles[row][col], [xOff, yOff])
        self.screen.blit(self.tiles[row][col2], [xOff + self.tile_width, yOff])
        self.screen.blit(self.tiles[row2][col], [xOff, yOff + self.tile_height])
        self.screen.blit(self.tiles[row2][col2], [xOff + self.tile_width, yOff + self.tile_height])

        self.surface = self.screen.copy()

    
    def set_colour(self, colour):
        self.colour = parse_colour(colour)
        self.screen.fill(self.colour)
        pygame.display.update()
        self.surface = self.screen.copy()

class Menu(Screen):
    def __init__(self, name, sizes, background_image, background_music, caption, icon):
        super().__init__(name, sizes, background_image, background_music, caption, icon)
  

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = 16

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        if self.text != '':
            font = pygame.font.Font('freesansbold.ttf', self.font_size )
            text = font.render(self.text, 1, (255, 255, 255))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def get_and_load_sprits(filename, character):
    current_path = os.getcwd()
    path = os.path.join(current_path, "images", "sprits", character.name, "resized", f"{filename}", "")
    sprits = []
    for sprit in os.listdir(path):
        sprit = os.path.join(path, f"{sprit}")
        sprits.append(pygame.image.load(sprit))

    return (sprits, len(sprits))


class Character(object):
    
    def __init__(self, name, position):
        self.name = name  # same with folder name of sprits
        self.x = position[0]
        self.y = position[1]
        self.width = 64
        self.height = 64

        self.walk_speed = 3
        self.run_speed = self.walk_speed + 4
        self.speed = self.walk_speed
        self.jump_power = 10 
        self.jump_step = self.jump_power # jump_step must take same value with the INITIAL value of jump_power

        self.points = 0
        self.health = 100
        self.controllers = {"jump": pygame.K_UP, 
                            "right": pygame.K_RIGHT, 
                            "left": pygame.K_LEFT,
                            "run": pygame.K_RSHIFT}
        
        self.is_ = {"right":False, "left":False, "jump":False, "fall":False, "run":False, "dead":False}
        self.counts = {"walk":0, "idle":0, "jump":0, "run":0, "dead":0}
        self.last_direction = "right"
        
        self.sprits_r = {"Walk":get_and_load_sprits("Walk", self),
                       "Run":get_and_load_sprits("Run", self),
                       "Idle":get_and_load_sprits("Idle", self),
                       "Jump":get_and_load_sprits("Jump", self),
                       "Dead":get_and_load_sprits("Dead", self)
                       }

        self.sprits_l = {"Walk":[list(map(lambda img:pygame.transform.flip(img, True, False), self.sprits_r["Walk"][0])), self.sprits_r["Walk"][1]], 
                        "Run":[list(map(lambda img:pygame.transform.flip(img, True, False), self.sprits_r["Run"][0])), self.sprits_r["Run"][1]], 
                        "Idle":[list(map(lambda img:pygame.transform.flip(img, True, False), self.sprits_r["Idle"][0])), self.sprits_r["Idle"][1]], 
                        "Jump":[list(map(lambda img:pygame.transform.flip(img, True, False), self.sprits_r["Jump"][0])), self.sprits_r["Jump"][1]], 
                        "Dead":[list(map(lambda img:pygame.transform.flip(img, True, False), self.sprits_r["Dead"][0])), self.sprits_r["Dead"][1]]    
                        }
        self.sprits = self.sprits_r
        
        self.visible = True
        self.screen = main_menu
        



    @property
    def collision(self): return pygame.Rect(self.hitbox)
    @collision.setter
    def collision(self, value): self.collision = value

    @property
    def hitbox(self): return (self.x + 10, self.y + 5, 45, 60)
    @hitbox.setter
    def hitbox(self, value): self.hitbox = value

    def walkto(self, direction):
        if direction == "right" and self.x < self.screen.width - (self.width - 5):
            self.x += self.speed
        elif direction == "left" and self.x > 0 - 5:
            self.x -= self.speed

    def jumpto(self):
        if self.is_["jump"]:
            if self.jump_step >= -self.jump_power:
                    self.y -= (self.jump_step * abs(self.jump_step)) * 0.33
                    self.jump_step -= 1
                    
                    if self.jump_step <= 0:
                        self.screen.background.scroll(0, int(-self.speed * 2))
                        #self.is_["fall"] = True
                    else:
                        self.screen.background.scroll(0, int(self.speed * 4))

                    if self.jump_power >= 20 and self.jump_step == -self.jump_power - 1:
                        self.is_["dead"] = True
            else: 
                self.jump_step = self.jump_power
                self.is_["jump"] = False
                self.is_["fall"] = False


    def draw(self, window):
        if not self.visible: return 

        if self.counts["idle"] + 1 >= self.sprits["Idle"][1] * 4:
            self.counts["idle"] = 0
        if self.counts["walk"] + 1 >= self.sprits["Walk"][1] * 4:
            self.counts["walk"] = 0
        if self.counts["jump"] +1 >= self.sprits["Jump"][1] * 4:
            self.counts["jump"] = 0
        if self.counts["run"] + 1 >= self.sprits["Run"][1] * 4:
            self.counts["run"] = 0
        if self.counts["dead"] + 1 >= self.sprits["Dead"][1] * 4:
            self.counts["dead"] = 0
            global main_menu_loop 
            main_menu_loop = False
            
        if self.is_["dead"]:
            window.blit(self.sprits["Dead"][0][self.counts["dead"]//4], (self.x, self.y))
            self.counts["dead"] += 1
        else:
            if self.is_["jump"]:
                # self.jumpto()
                window.blit(self.sprits["Jump"][0][self.counts["jump"]//4], (self.x, self.y))
            if self.is_["right"]:
                # self.walkto("right")
                if self.is_["run"]:
                    window.blit(self.sprits["Run"][0][self.counts["run"]//4], (self.x, self.y))
                    self.counts["run"] += 1
                else:
                    window.blit(self.sprits["Walk"][0][self.counts["walk"]//4], (self.x, self.y))
                    self.counts["walk"] += 1
                    
            elif self.is_["left"]:
                # self.walkto("left")
                if self.is_["run"]:
                    window.blit(self.sprits["Run"][0][self.counts["run"]//4], (self.x, self.y))
                    self.counts["run"] += 1
                else:
                    window.blit(self.sprits["Walk"][0][self.counts["walk"]//4], (self.x, self.y))
                    self.counts["walk"] += 1
            
            else:
                window.blit(self.sprits["Idle"][0][self.counts["idle"]//4], (self.x, self.y))
                self.counts["idle"] += 1
        
        pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)

    def keyboard_behaviours(self):
        
        if self.is_["right"] == False and self.is_["left"] == False:
            self.last_direction = self.last_direction

        else:
            if self.is_["right"]:
                self.last_direction = "right"
                self.sprits = self.sprits_r
                
            elif self.is_["left"]:
                self.last_direction = "left"
                self.sprits = self.sprits_l

        keys = pygame.key.get_pressed()
        
        if keys[self.controllers["right"]]:
            self.is_["right"] = True
            self.is_["left"] = False
        elif keys[self.controllers["left"]]:
            self.is_["right"] = False
            self.is_["left"] = True
        else:
            self.is_["right"] = False
            self.is_["left"] = False
            self.counts["walk"] = 0
        if keys[self.controllers["run"]]:
            self.speed = self.run_speed
            self.is_["run"] = True
        else:
            self.speed = self.walk_speed
            self.is_["run"] = False
            self.counts["run"] = 0


        if keys[self.controllers["jump"]]:
            self.is_["jump"] = True
        
        
    def action(self):
        
        if self.is_["jump"]:
            self.jumpto()
        if self.is_["right"]:
            if self.screen.width - self.x <= self.screen.width / 4:
                self.screen.background.scroll(-self.speed, 0)
            else:
                self.walkto("right")
            # self.walkto(self.last_direction)
            # self.screen.background.scroll(-self.speed, 0) 
        elif self.is_["left"]:

            if self.x <= self.screen.width / 4:
                self.screen.background.scroll(self.speed, 0)
            else:
                self.walkto("left")
            # self.walkto(self.last_direction)
            # self.screen.background.scroll(self.speed, 0)
        else:
            self.screen.background.scroll(0, 0)
            



class SpaceShip(object):

    class Thruster(object):
        def __init__(self, ship):
            self.ship  = ship
            self.sprit = ship.sprits["thruster_idle"]
    
        
        @property
        def x(self): return self.ship.x + - 115
        @x.setter
        def x(self, value): self.x = value
        @property
        def y(self): return self.ship.y - 27
        @y.setter
        def y(self, value): self.y = value

        def draw(self):
            self.ship.screen.blit(self.sprit, (self.x, self.y))
        
        def action(self):
            if self.ship.is_["right"] or self.ship.is_["left"]:
                self.sprit = self.ship.sprits["thruster_power"]
            else:
                self.sprit = self.ship.sprits["thruster_idle"]


    def __init__(self, name, pilot, screen, position):
        self.name = name
        self.x = position[0]
        self.y = position[1]
        self.speed = 30
        self.sensvity = 5
        self.angle = 0
        self.angle_ = False
        self.origin = (self.x, self.y)
        self.pilot = pilot
        self.screen = screen
        
        self.is_ = {"right":False, "left":False}
        aux_controllers = self.pilot.controllers
        aux_controllers.update({"crouch": pygame.K_DOWN})
        self.controllers = aux_controllers
        self.sprits = {
                        "ship":pygame.transform.scale(load_image("4_Red.png"), (128, 128)), 
                        "thruster_idle":pygame.transform.scale(load_image("1.png"), (64, 64)), 
                        "thruster_power":pygame.transform.scale(load_image("2.png"), (64, 64))
                        }

        self.rect = self.sprits["ship"].get_rect()
        self.thruster = self.Thruster(self)
        self.location = self.sprits["ship"].get_rect(center=self.rect.center)
        self.image_copy = self.sprits["ship"]



    def set_origin(self, image, pos, originPos, angle, rotate = False):
        #if self.angle_ == False: return self.origin
        # calcaulate the axis aligned bounding box of the rotated image
        w, h       = image.get_size()
        box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]
        min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
        max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

        # calculate the translation of the pivot 
        pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
        pivot_rotate = pivot.rotate(angle)
        pivot_move   = pivot_rotate - pivot

        # calculate the upper left origin of the rotated image
        origin = ((pos[0] - originPos[0] + min_box[0] - pivot_move[0]), (pos[1] - originPos[1] - max_box[1] + pivot_move[1]))

        self.origin = origin

        return

    def rotate(self, surf, image, angle):
        self.image_copy = pygame.transform.rotate(image, angle)
        
        # rotate and blit the image
        # surf.blit(self.image_copy, self.origin)

        # draw rectangle around the image
        pygame.draw.rect(surf, (255, 0, 0), (*self.origin, *self.image_copy.get_size()),2)
        
        return

    def draw(self):
        
        w, h = self.sprits["ship"].get_size()
        
        if self.angle_:
            self.set_origin(self.sprits["ship"], (self.x, self.y), (w/2, h/2), self.angle)
            self.rotate(self.screen.screen, self.sprits["ship"], self.angle)
        else:
            self.set_origin(self.sprits["ship"], (self.x, self.y), (w/2, h/2), 0)

        self.screen.blit(self.image_copy, self.origin)
        self.thruster.draw()
        
    def keyboard_behaviours(self):
        #if self.angle >= 360: self.angle = 0

        keys = pygame.key.get_pressed()
        if keys[self.controllers["jump"]]:
            angle_rad = math.radians(self.angle % 360)
            self.x += math.cos(angle_rad) * self.speed
            self.y -= math.sin(angle_rad) * self.speed

        elif keys[self.controllers["crouch"]]:
            self.x -= self.speed
        else:
            pass

        if keys[self.controllers["right"]]:
            self.angle_ = True
            self.angle -= self.sensvity
        elif keys[self.controllers["left"]]:
            self.angle_ = True
            self.angle += self.sensvity

        else:
            self.angle_ = False

        

        # if keys[self.controllers["run"]]:
        #     self.speed = self.run_speed
        #     self.is_["run"] = True
        # else:
        #     self.speed = self.walk_speed
        #     self.is_["run"] = False
        #     self.counts["run"] = 0


        # if keys[self.controllers["jump"]]:
        #     self.is_["jump"] = True


    def action(self):
        self.thruster.action()
        
        if self.is_["right"]:
            if self.screen.width - self.x <= self.screen.width / 4:
                self.screen.background.scroll(-self.speed, 0)

            # self.walkto(self.last_direction)
            # self.screen.background.scroll(-self.speed, 0) 
        elif self.is_["left"]:

            if self.x <= self.screen.width / 4:
                self.screen.background.scroll(self.speed, 0)
            else:
                self.x -= self.speed
            # self.walkto(self.last_direction)
            # self.screen.background.scroll(self.speed, 0)
        else:
            self.screen.background.scroll(0, 0)





def is_collision(rect1, rect2):

    return rect1.colliderect(rect2)

# Initialize the pygame
pygame.init()

# Create the screen
main_menu = Menu("main", [800, 600], "space.png", "background_music.wav", "MOOM", "icon")
main_menu.background.set_tiles([[main_menu.background_image]])

# Load media for screen
main_menu.load("music")
animated_moon = pygame.image.load(os.path.join("images", "moon.png")).convert_alpha()

# Display the screen
main_menu.set_("screen") 
main_menu.set_("caption")

# Background music
#mixer.music.play(-1)

# Buttonschar1.hitbox = (char1.x + 20, char1.y, 15, 60)
play_button = Button((0, 100, 0), 20, 300, 120, 80, 'Play')
settings_button = Button((0, 100, 0), 20, 350, 120, 80, 'Options')
leave_button = Button((0, 100, 0), 20, 400, 120, 80, 'Leave')

# Character
char = Character("girl", [350, 400])
char.jump_step = char.jump_power = 10

char1 = Character("boy", [400, 400])
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
    char.keyboard_behaviours()
    char1.keyboard_behaviours()
    char.action()
    char1.action()
    ship.keyboard_behaviours()
    ship1.keyboard_behaviours()
    ship.action()
    ship1.action()
        
    if is_collision(char.collision, char1.collision):
        print('hi')
    redraw_game_screen(char, char1, window=main_menu)
    
    while play_loop:
        print("Crash crash crash C:")

