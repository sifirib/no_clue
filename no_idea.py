import pygame
from pygame import mixer
import os
import math
# from Background import Background 
# from Screen import Screen, Menu
# from Button import Button
# from Character import Character
# from SpaceShip import SpaceShip

def set_origin(obj, image, pos, origin_pos, angle, rotate = False):
    #if self.angle_ == False: return self.origin
    # calcaulate the axis aligned bounding box of the rotated image
    w, h       = image.get_size()
    box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

    # calculate the translation of the pivot 
    pivot        = pygame.math.Vector2(origin_pos[0], -origin_pos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = ((pos[0] - origin_pos[0] + min_box[0] - pivot_move[0]), (pos[1] - origin_pos[1] - max_box[1] + pivot_move[1]))

    obj.origin = origin
    # obj.rect.center = obj.origin

    return

def rotate(obj, surf, image, angle):
    obj.sprit_copy = pygame.transform.rotate(image, angle)
    
    # rotate and blit the image
    # surf.blit(self.sprit_copy, self.origin)

    # draw rectangle around the image
    # pygame.draw.rect(surf, (255, 0, 0), (*obj.origin, *obj.sprit_copy.get_size()), 2)
    
    return

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


def get_and_load_sprits(filename, character, sizes=(0, 0)):
    
    # Resizing sprits in game will take time... so, using already resized sprites will be more sensible in this case but will take more storage 
    
    current_path = os.getcwd()
    path = os.path.join(current_path, "images", "sprits", character.name, "resized", f"{filename}", "")

    def proc(sprit, sizes):
        global path

        if sizes == (0, 0):

            return pygame.image.load(sprit)
        else:
            path = os.path.join(current_path, "images", "sprits", character.name, "original", f"{filename}", "")

            return pygame.transform.scale(pygame.image.load(sprit), sizes)
    
    sprits = []
    for sprit in os.listdir(path):
        sprit = os.path.join(path, f"{sprit}")
        sprits.append(proc(sprit, sizes))

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
        
        self.sprits_r = {"Walk":get_and_load_sprits("Walk", self), # "Walk":get_and_load_sprits("Walk", self, (64, 64))
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
            if self.screen.width - self.x <= self.screen.width / 12:
                self.screen.background.scroll(-self.speed, 0)
            else:
                self.walkto("right")
            # self.walkto(self.last_direction)
            # self.screen.background.scroll(-self.speed, 0) 
        elif self.is_["left"]:

            if self.x <= self.screen.width / 12:
                self.screen.background.scroll(self.speed, 0)
            else:
                self.walkto("left")
            # self.walkto(self.last_direction)
            # self.screen.background.scroll(self.speed, 0)
        else:
            self.screen.background.scroll(0, 0)
            

class Planet(object):

    def __init__(self):
        self.air_friction = 0.015
        self.gravity = 10

class SpaceShip(object):

    class Thruster(object):
        def __init__(self, ship):
            self.ship  = ship
            # self.sprit = ship.sprits["thruster_idle"]
            self.sprit_ = self.sprit
            self.origin = (self.x, self.y)
            self.sprit_copy_ = self.sprit
        
        @property
        def sprit(self):
            if self.ship.is_["forward"]: return self.ship.sprits["thruster_power"]
            else: return self.ship.sprits["thruster_idle"]
        # @sprit.setter
        # def sprit(self, value): self.sprit_ = value

        @property
        def x(self): return self.ship.rect.center[0] - (self.ship.offset("thruster")[0] * math.cos(self.ship.angle_rad) + self.ship.offset("thruster")[1] * math.sin(self.ship.angle_rad))
        @property
        def y(self): return self.ship.rect.center[1] - (self.ship.offset("thruster")[0] * -math.sin(self.ship.angle_rad) + self.ship.offset("thruster")[1] * math.cos(self.ship.angle_rad))
        
        @property
        def rect(self): return self.sprit_copy.get_rect(center=(self.origin))
        # @rect.setter
        # def rect(self, value): self.rect = value
        
        @property
        def sprit_copy(self):
            w, h = self.sprit_copy_.get_size()
        
            if self.ship.angle_:
                set_origin(self, self.sprit, (self.x, self.y), (w/2, h/2), self.ship.angle)
            else:
                set_origin(self, self.sprit, (self.x, self.y), (w/2, h/2), 0)

            rotate(self, self.ship.screen.screen, self.sprit, self.ship.angle)

            return self.sprit_copy_
            
        @sprit_copy.setter
        def sprit_copy(self, value): self.sprit_copy_ = value


        
        def draw(self):
            self.ship.screen.blit(self.sprit_copy, self.origin)


        def action(self):            
            pass

    def __init__(self, name, pilot, screen, position):
        self.name = name
        self.x = position[0]
        self.y = position[1]
        self.old_x = self.x
        self.old_y = self.y
        self.vel = 0
        self.normal_speed = 10
        self.max_speed = 20
        self.accel = 2
        self.sensvity = 7
        self.angle = 0
        self.angle_ = False
        self.origin = (self.x, self.y)
        self.pilot = pilot
        self.screen = screen
        self.poses = [[self.x, self.y]]
        

        self.is_ = {"right":0, "left":0, "up":0, "down":0, "forward":0, "backward":0}

        aux_controllers = self.pilot.controllers
        aux_controllers.update({"crouch": pygame.K_DOWN})
        self.controllers = aux_controllers

        self.sprits = {
                        "ship":pygame.transform.scale(load_image(self.name), (128, 128)), 
                        "thruster_idle":pygame.transform.scale(load_image("1.png"), (64, 64)), 
                        "thruster_power":pygame.transform.scale(load_image("2.png"), (64, 64))
                        }
        self.sprit_copy = self.sprits["ship"]
        self.offsets = {"thruster":(82, -7)}
        self.thruster = self.Thruster(self)
        
        # self.location = self.sprits["ship"].get_rect(center=self.rect.center)
        

    # @property
    # def offsets(self): 
    #     offsets = {"thruster":self.thrus}
    #     return 

    def offset(self, key):

        return self.offsets[key]


    @property
    def speed(self): return abs(self.vel)
    @speed.setter
    def speed(self, value): self.speed = value

    @property
    def pitch(self): return self.is_["forward"] - self.is_["backward"]
    @pitch.setter
    def pitch(self, value): self.pitch = value

    @property
    def angle_rad(self): return math.radians(self.angle)
    @angle_rad.setter
    def angle_rad(self, value): self.angle_rad = value

    @property
    def rect(self): return self.sprit_copy.get_rect(center=(self.x, self.y))
    @rect.setter
    def rect(self, value): self.rect = value

    

    def draw(self):

        self.screen.blit(self.sprit_copy, self.origin)
        self.thruster.draw()
        
    def keyboard_behaviours(self):
        #if self.angle >= 360: self.angle = 0
        
        keys = pygame.key.get_pressed()
        if keys[self.controllers["jump"]]:
            self.is_["backward"] = 0
            self.is_["forward"] = 1
            if self.speed < self.max_speed:
                self.vel += self.accel
                if self.speed > self.max_speed:
                    self.vel = self.max_speed

        elif keys[self.controllers["crouch"]]:
            self.is_["backward"] = 1
            self.is_["forward"] = 0
            if self.speed < self.max_speed:
                self.vel -= self.accel
                if self.speed > self.max_speed:
                    self.vel = -self.max_speed

        
        else:
            self.is_["backward"] = 0
            self.is_["forward"] = 0
            pass
            
       
        if keys[self.controllers["right"]]:
            self.angle_ = True
            self.angle -= self.sensvity
        elif keys[self.controllers["left"]]:
            self.angle_ = True
            self.angle += self.sensvity

        else:
            self.angle_ = False



    def action(self):
        self.thruster.action()
        self.poses.append([self.x, self.y])
         


        w, h = self.sprits["ship"].get_size()
        
        if self.angle_:
            set_origin(self, self.sprits["ship"], (self.x, self.y), (w/2, h/2), self.angle)
            rotate(self, self.screen.screen, self.sprits["ship"], self.angle)
        else:
            set_origin(self, self.sprits["ship"], (self.x, self.y), (w/2, h/2), 0)



        if self.pitch == 0:
            
            if self.vel > 0:
                self.vel -= self.max_speed * earth.air_friction
                if self.vel < 0:
                    self.vel = 0
            
            elif self.vel < 0:
                self.vel += self.max_speed * earth.air_friction
                if self.vel > 0:
                    self.vel = 0 
            
            else:
                # self.vel = 0
                pass

        else:
            pass

        
        # if (math.cos(self.angle_rad)) > 0:
        #     self.is_["right"] = 1
        #     self.is_["left"] = 0
        # elif (math.cos(self.angle_rad)) < 0:
        #     self.is_["right"] = 0
        #     self.is_["left"] = 1
        # else:
        #     self.is_["right"] = 0
        #     self.is_["left"] = 0
        # if (math.sin(self.angle_rad)) > 0:
        #     self.is_["up"] = 1
        #     self.is_["down"] = 0
        # elif (math.sin(self.angle_rad)) < 0:
        #     self.is_["up"] = 0
        #     self.is_["down"] = 1
        # else:
        #     self.is_["up"] = 0
        #     self.is_["down"] = 0
        
        print(ship.rect.top, ship.rect.bottom)
        if (self.screen.width - self.rect.right <= self.screen.width / 12) or (self.rect.left <= self.screen.width / 12) or (self.rect.top <= self.screen.height / 12) or (self.screen.height - self.rect.bottom <= self.screen.height / 12):
            self.screen.background.scroll(-int(math.cos(self.angle_rad) * self.vel), int(math.sin(self.angle_rad) * self.vel))
        else:
            self.x += math.cos(self.angle_rad) * self.vel
            self.y -= math.sin(self.angle_rad) * self.vel
            self.screen.background.scroll(0, 0)
        
        


def is_collision(rect1, rect2):

    return rect1.colliderect(rect2)

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
#mixer.music.play(-1)

# Buttonschar1.hitbox = (char1.x + 20, char1.y, 15, 60)
play_button = Button((0, 100, 0), 20, 300, 120, 80, 'Play')
settings_button = Button((0, 100, 0), 20, 350, 120, 80, 'Options')
leave_button = Button((0, 100, 0), 20, 400, 120, 80, 'Leave')

#Planet
earth = Planet()

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
        
