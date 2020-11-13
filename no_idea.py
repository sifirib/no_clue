import pygame
from pygame import mixer
import os


class Screen:
    def __init__(self, name, sizes, background_image, background_music, caption, icon):
        self.name = name
        self.width = sizes[0]
        self.height = sizes[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.background_image = background_image
        self.background_music = background_music
        self.caption = caption
        self.icon = icon
    
    def load(self, what):
        if what == "music":
            self.background_music = mixer.music.load(self.background_music)
        elif what == "image":
            self.background_image = pygame.image.load(self.background_image)
            
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
            gog = pygame.font.SysFont('comicsans', 40)
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
    path = os.path.join(current_path, "sprits", character.name, f"{foldername}", "")
    sprits = []
    for sprit in os.listdir(path):
        sprit = os.path.join(path, f"{sprit}")
        sprits.append(pygame.image.load(sprit))
    return (sprits, len(sprits))


class Character:
    
    def __init__(self, name, position):
        self.name = name # same with folder name of sprits
        self.x = position[0]
        self.y = position[1]
        self.width = 64
        self.height = 64
        self.walk_speed = 3
        self.run_speed = self.walk_speed + 4
        self.speed = self.walk_speed
        self.jump_power = 10
        self.jump_step = 10 # must be same number with jump_power
        
        self.sprits = {"Walk":get_and_load_sprits("Walk", self),
                       "Run":get_and_load_sprits("Run", self),
                       "Idle":get_and_load_sprits("Idle", self),
                       "Jump":get_and_load_sprits("Jump", self),
                       "Dead":get_and_load_sprits("Dead", self)
                       }
        self.points = 0
        self.health = 100
        self.controllers = {"jump": pygame.K_UP, 
                            "right": pygame.K_RIGHT, 
                            "left": pygame.K_LEFT,
                            "run": pygame.K_RSHIFT}
        self.is_ = {"right":False, "left":False, "jump":False, "run":False}
        self.counts = {"walk":0, "idle":0, "jump":0, "run":0}
        
        self.hitbox = (self.x + 20, self.y, 28, 60)
        self.collision = pygame.Rect(self.hitbox)
        
        

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
            else: 
                self.jump_step = self.jump_power
                self.is_["jump"] = False
        
        
    def draw(self, window):
        
        if self.counts["idle"] + 1 >= self.sprits["Idle"][1] * 3:
            self.counts["idle"] = 0
        if self.counts["walk"] + 1 >= self.sprits["Walk"][1] * 3:
            self.counts["walk"] = 0
        if self.counts["jump"] +1 >= self.sprits["Jump"][1] * 3:
            self.counts["jump"] = 0
        if self.counts["run"] + 1 >= self.sprits["Run"][1] * 3:
            self.counts["run"] = 0
            
        if self.is_["right"]:
            self.walkto("right")
            if self.is_["run"]:
                window.blit(self.sprits["Run"][0][self.counts["run"]//3], (self.x, self.y))
                self.counts["run"] += 1
            else:
                window.blit(self.sprits["Walk"][0][self.counts["walk"]//3], (self.x, self.y))
                self.counts["walk"] += 1
        elif self.is_["left"]:
            self.walkto("left")
            if self.is_["run"]:
                window.blit(self.sprits["Run"][0][self.counts["run"]//3], (self.x, self.y))
                self.counts["run"] += 1
            else:
                window.blit(self.sprits["Walk"][0][self.counts["walk"]//3], (self.x, self.y))
                self.counts["walk"] += 1
        elif self.is_["jump"]:
            self.jumpto()
            window.blit(self.sprits["Jump"][0][self.counts["jump"]//3], (self.x, self.y))
        else:
            window.blit(self.sprits["Idle"][0][self.counts["idle"]//3], (self.x, self.y))
            self.counts["idle"] += 1
        
        self.hitbox = (self.x + 10, self.y + 5, 45, 60)
        # pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        
        
        
    def keyboard_behaviours(self):
        keys = pygame.key.get_pressed()

        if not self.is_["jump"]:
        
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
                self.is_["left"] = False
                self.is_["right"] = False
                self.counts["walk"] = 0
    
    
    
def is_collision(rect1, rect2):
    y = False
    if rect1.colliderect(rect2):
        y = True
    return y
        


# Initialize the pygame
pygame.init()

# Create the screen
main_menu = Menu("main", [800, 600], "space.png", "background_music.wav", "caption", "icon")

# Load media for screen
main_menu.load("image")
main_menu.load("music")
animated_moon = pygame.image.load("moon.png")


# Display the screen
main_menu.set_("screen") 
main_menu.set_("caption")

# Background music
#mixer.music.play(-1)

# Buttons
play_button = Button((0, 100, 0), 20, 300, 120, 80, 'Play')
settings_button = Button((0, 100, 0), 20, 350, 120, 80, 'Options')
leave_button = Button((0, 100, 0), 20, 400, 120, 80, 'Leave')


# Character

char = Character("girl", [100, 400])
char1 = Character("boy", [200, 400])
char1.walk_speed = 4
char1.jump_step = 12
char1.jump_power = 12
char1.controllers = {"jump": pygame.K_w, 
                     "right": pygame.K_d, 
                     "left": pygame.K_a,
                     "run": pygame.K_LSHIFT}


def redraw_game_screen(*args, window):
    chars = args
    window.blit(window.background_image, (0, 0))
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
    redraw_game_screen(char1, char, window=main_menu)
    
    while play_loop:
        print(".")
        
           
