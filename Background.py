import pygame
import os

def load_image(file_name, useColorKey=False):
    current_path = os.getcwd()
    file_ = os.path.join(current_path, "images", file_name)

    if os.path.isfile(file_):
        image = pygame.image.load(file_)
        image = image.convert_alpha()
        # Return the image
        return image
    else:
        raise Exception("Error loading image: " + file_name + " - Check filename and path?")

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
