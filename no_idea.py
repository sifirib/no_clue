import pygame
from pygame import mixer
import os


class Screen:
    def __init__(self, name, sizes, background_image, background_music, caption, icon):
        self.name = name
        self.x = self.y = 0
        self.width = sizes[0]
        self.height = sizes[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = background_image
        self.y2 = self.height  #self.background_image.get_height()
        self.x2 = self.width   #self.background_image.get_width()
        self.background_music = background_music
        self.caption = caption
        self.icon = icon
    
    def load(self, what):
        if what == "music":
            self.background_music = mixer.music.load(self.background_music)
        elif what == "image":
            self.background_image = pygame.image.load(self.background_image).convert()
            
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

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def get_and_load_sprits(foldername, character):
    current_path = os.getcwd()
    path = os.path.join(current_path, "sprits", character.name, "resized", f"{foldername}", "")
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
        
        self.is_ = {"right":False, "left":False, "jump":False, "run":False, "dead":False}
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

    # @property 
    # def run_speed(self): return self.walk_speed + 4
    # @run_speed.setter
    # def run_speed(self, value): self.run_speed = value

    @property
    def collision(self): return pygame.Rect(self.hitbox)
    @collision.setter
    def collision(self, value): self.collision = value

    @property
    def hitbox(self): return (self.x + 10, self.y + 5, 45, 60)
    @hitbox.setter
    def hitbox(self, value): self.hitbox = value

    def walkto(self, direction):
        if direction == "right" and self.x < main_menu.width - (self.width - 5):
            self.x += self.speed
        elif direction == "left" and self.x > 0 - 5:
            self.x -= self.speed

    def jumpto(self):
        if self.is_["jump"]:
            if self.jump_step >= -self.jump_power:
                    self.y -= (self.jump_step * abs(self.jump_step)) * 0.33
                    self.jump_step -= 1
                    
                    if self.jump_power >= 20 and self.jump_step == -self.jump_power - 1:
                        self.is_["dead"] = True
            else: 
                self.jump_step = self.jump_power
                self.is_["jump"] = False
    
    
    def draw(self, window):
        
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
                self.jumpto()
                window.blit(self.sprits["Jump"][0][self.counts["jump"]//4], (self.x, self.y))
            if self.is_["right"]:
                self.walkto("right")
                if self.is_["run"]:
                    window.blit(self.sprits["Run"][0][self.counts["run"]//4], (self.x, self.y))
                    self.counts["run"] += 1
                else:
                    window.blit(self.sprits["Walk"][0][self.counts["walk"]//4], (self.x, self.y))
                    self.counts["walk"] += 1
                    
            elif self.is_["left"]:
                self.walkto("left")
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

                if main_menu.width - self.x <= main_menu.width / 3:
                    main_menu.x -= self.speed * 3
                    main_menu.x2 -= self.speed * 3
            else:
                self.last_direction = "left"
                self.sprits = self.sprits_l
                if self.x <= main_menu.width / 3:
                    main_menu.x += self.speed * 3
                    main_menu.x2 += self.speed * 3
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

        if not self.is_["jump"]:
            if keys[self.controllers["jump"]]:
                self.is_["jump"] = True
                self.is_["left"] = False
                self.is_["right"] = False
                self.counts["walk"] = 0
                main_menu.y += self.jump_power * 3
                main_menu.y2 += self.jump_power * 3
                
def is_collision(rect1, rect2):

    return rect1.colliderect(rect2)

# Initialize the pygame
pygame.init()

# Create the screen
main_menu = Menu("main", [800, 600], "space.png", "background_music.wav", "caption", "icon")

# Load media for screen
main_menu.load("image")
main_menu.y2 = main_menu.background_image.get_height()
main_menu.x2 = main_menu.background_image.get_width()
main_menu.load("music")
animated_moon = pygame.image.load("moon.png")
#animated_moon = pygame.image.load("moon.png").convert_alpha()


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
char = Character("girl", [100, 400])
char.jump_step = char.jump_power = 10

char1 = Character("boy", [200, 400])
char1.run_speed = char1.walk_speed + 6
char1.jump_step = char1.jump_power = 12
char1.controllers = {"jump": pygame.K_w, 
                     "right": pygame.K_d, 
                     "left": pygame.K_a,
                     "run": pygame.K_LSHIFT}


def redraw_game_screen(*args, window):
    chars = args
    #window.screen.blit(window.background_image, (x_, y_))
    window.screen.blit(window.background_image, (x_, 0))
    #window.screen.blit(window.background_image, (window.x2, 0))
    window.screen.blit(animated_moon, (moon_width, moon_height))
    
    for char in chars:
        char.draw(window.screen)
        
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
    clock.tick(fps)

    # if main_menu.x < main_menu.background_image.get_width() * -1:  # If our bg is at the -width then reset its position
    #     main_menu.x = main_menu.background_image.get_width()
    # elif main_menu.x > main_menu.background_image.get_width(): # If our bg is at the -width then reset its position
    #     main_menu.x = main_menu.background_image.get_width() * -1
    # if main_menu.x2 < main_menu.background_image.get_width() * -1:
    #     main_menu.x2 = main_menu.background_image.get_width()
    # elif main_menu.x2 > main_menu.background_image.get_width():
    #     main_menu.x2 = 0

    # if main_menu.y < main_menu.background_image.get_height() * -1:  # If our bg is at the -height then reset its position
    #     main_menu.y = main_menu.background_image.get_height()
    # if main_menu.y2 < main_menu.background_image.get_height() * -1:
    #     main_menu.y2 = main_menu.background_image.get_height()

    x = main_menu.x % main_menu.background_image.get_width()
    x_ = x - main_menu.background_image.get_width()
    # y = main_menu.y % main_menu.background_image.get_height()
    # y_ = y - main_menu.background_image.get_height()
    if x < main_menu.width:
        main_menu.screen.blit(main_menu.background_image, (x, 0))
    # if y < main_menu.height:
    #     main_menu.screen.blit(main_menu.background_image, (0, y))

    
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
            if leave_button.isOver(pos):
                main_menu_loop = False
                pygame.quit()
                quit()
            if play_button.isOver(pos):
                play_loop = True
        
        if event.type == pygame.MOUSEMOTION:
            if play_button.isOver(pos):
                play_button.font_size = 20
            else:
                play_button.font_size = 16
            if leave_button.isOver(pos):
                leave_button.font_size = 20
            else:
                leave_button.font_size = 16
            if settings_button.isOver(pos):
                settings_button.font_size = 20
            else:
                settings_button.font_size = 16
                
        # KEYBOARD behaviours
        char.keyboard_behaviours()
        char1.keyboard_behaviours()
        
    if is_collision(char.collision, char1.collision):
        print('hi')
    redraw_game_screen(char, char1, window=main_menu)
    
    while play_loop:
        print("Crash crash crash C:")

