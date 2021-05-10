import pygame
import os
# import main

def get_and_load_sprits(foldername, character):
    current_path = os.getcwd()
    path = os.path.join(current_path, "images", "sprits", character.name, "resized", f"{foldername}", "")
    sprits = []
    for sprit in os.listdir(path):
        sprit = os.path.join(path, f"{sprit}")
        sprits.append(pygame.image.load(sprit))

    return (sprits, len(sprits))


class Character(object):

    def __init__(self, name, position, screen, planet):
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
        self.screen = screen
        self.planet = planet




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
