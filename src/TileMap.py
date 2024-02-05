# ===================== import ===================== #

import pygame
import csv
from Player import Player
from Enemy import Enemy

# ===================== tile ===================== #

class Tile(pygame.sprite.Sprite):
    """
    Class to create a single tile.
    """

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

# ===================== tilemap ===================== #
        
class TileMap(pygame.sprite.Sprite):
    """
    Class to create the tilemap with which other objects can interact.
    """
    
    def __init__(self, csvPath:str):
        super().__init__()
        self._tiles = []  
        self.enemyList = []  
        lst = self.readCSV( filePath = csvPath)
        
        for column in range(len(lst)):
            for row in range(len(lst[0])):
                if  lst[column][row] == "1":
                   tile = Tile("sprites/placeholder/Grass.png", row * 16, column * 16)
                   self._tiles.append(tile)
                if lst[column][row] == "2":
                   tile = Tile("sprites/placeholder/Dirt.png", row * 16, column * 16 )
                   self._tiles.append(tile)
                if lst[column][row] == "3":
                    self.enemy = Enemy(row*16,-50)
                    self.enemyList.append(self.enemy)
                   
        combined = Combined(self._tiles)
        self.image = combined.image
        self.rect = self.image.get_rect()
        
        for column in range(len(lst)):
            for row in range(len(lst[0])):
                if lst[column][row] == "0":
                    self.player = Player()
        
    def updateTilemapPosition(self):
        self.prev_x = self.rect.x
        self.prev_y = self.rect.y

    def readCSV(self, filePath:str)->list:
        data = [[]]
        try:
            file = open(filePath, "r")  
            data = list(csv.reader(file, delimiter=","))
            file.close()
        except:
            print("Can't read csv file")
        
        return data
    
# ===================== combined ===================== #
    
class Combined(pygame.sprite.Sprite):
    """
    Class to combine different sprites.
    """

    def __init__(self, sprites):
        super().__init__()
        # Combine the rects of the separate sprites.
        self.rect = sprites[0].rect.copy()
        for sprite in sprites[1:]:
            self.rect.union_ip(sprite.rect)

        # Create a new transparent image with the combined size.
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # Now blit all sprites onto the new surface.
        for sprite in sprites:
            self.image.blit(sprite.image, (sprite.rect.x-self.rect.left,
                                           sprite.rect.y-self.rect.top))