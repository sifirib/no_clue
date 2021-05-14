
class Entity(object):

    def __init__(self, name, position, screen, planet):
        self.name = name  # same with folder name of sprits
        self.x = position[0]
        self.y = position[1]
        self.width = 64
        self.height = 64

        self.vel = 0
        self.accel = 0
        self.mass = 0

        self.sprits = None

        # self.rect = self.sprits_r["Idle"][0][0].get_rect()
        
        self.visible = True
        self.screen = screen
        self.planet = planet

    # @property
    # def hitbox(self): return (self.x + 10, self.y + 5, 45, 60)
    # @hitbox.setter
    # def hitbox(self, value): self.hitbox = value

    # @property
    # def collision(self): return pygame.Rect(self.hitbox)
    # @collision.setter
    # def collision(self, value): self.collision = value

    