from Entity import Entity
import pygame
import math
from Background import load_image
from shared import set_origin, rotate


class SpaceShip(Entity):

    class Thruster(Entity):
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

    def __init__(self, name, position, screen, planet, pilot):
        super().__init__(name, position, screen, planet)

        self.old_x = self.x
        self.old_y = self.y
        self.normal_speed = 10
        self.max_speed = 20
        self.accel = 2
        self.sensvity = 7
        self.angle = 0
        self.angle_ = False
        self.origin = (self.x, self.y)
        self.pilot = pilot
        self.poses = [[self.x, self.y]]
        self.planet = self.pilot.planet


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
                self.vel -= self.max_speed * self.planet.air_friction
                if self.vel < 0:
                    self.vel = 0

            elif self.vel < 0:
                self.vel += self.max_speed * self.planet.air_friction
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

        # print(ship.rect.top, ship.rect.bottom)
        if (self.screen.width - self.rect.right <= self.screen.width / 12) or (self.rect.left <= self.screen.width / 12) or (self.rect.top <= self.screen.height / 12) or (self.screen.height - self.rect.bottom <= self.screen.height / 12):
            self.screen.background.scroll(-int(math.cos(self.angle_rad) * self.vel), int(math.sin(self.angle_rad) * self.vel))
        else:
            self.x += math.cos(self.angle_rad) * self.vel
            self.y -= math.sin(self.angle_rad) * self.vel
            self.screen.background.scroll(0, 0)
