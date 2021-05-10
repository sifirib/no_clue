import pygame
import os
from pygame import mixer
from Background import *

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



class Menu(Screen):
    def __init__(self, name, sizes, background_image, background_music, caption, icon):
        super().__init__(name, sizes, background_image, background_music, caption, icon)
