# ===================== import ===================== #

import pygame
from TileMap import TileMap
from Player import Player

# ===================== Main ===================== #

class Game():
    """
    Class that fuses all of the subparts together for the game to be playable.
    """

    def __init__(self, __screenResolution, __currentLevel, __background):
        pygame.init()
        self.__screenResolution = __screenResolution
        self.__tileMap = TileMap(__currentLevel)
        self.__hurtMap = self.__tileMap.gethurtmap()
        self.__player = Player()
        self.__allSprites = pygame.sprite.Group()
        self.__allSprites.add(self.__tileMap)
        self.__allSprites.add(self.__player)
        self.__allSprites.add(self.__player.verticalCollisionBox)
        self.__allSprites.add(self.__player.horizontalCollisionBox)
        self.__background = pygame.image.load(__background)
        self.__background = pygame.transform.scale(self.__background,(self.__screenResolution))

    def resetHurtmap(self):
        """
        Method to reset the hurtmap.
        """
        
        self.__hurtMap = None

    def drawGameFrame(self):
        """
        Method to blit the game on the screen.
        """
        
        self.__allSprites.update()
        
        # camera - calculate the offset
        playerOffsetX = self.__screenResolution.x // 6 - self.__player.rect.centerx # more on the left site
        playerOffsetY = self.__screenResolution.y // 2 - self.__player.rect.centery # center
        
        # camera - move all sprites in the other direction
        for __sprite in self.__allSprites:
            __sprite.rect.x += playerOffsetX
            __sprite.rect.y += playerOffsetY

        # draws the current frame on the screen
        self.__screen.blit(self.__background, (0, 0))
        self.__allSprites.draw(self.__screen)
        #TODO UI health
        #TODO UI score
        pygame.display.flip()

# ============== game loop ============== #

    def run(self, __input, __screen):
        """
        Method that lets the game update and run in one.
        """

        # runs all of Game.py main functions
        self.__screen = __screen
        self.__input = __input
        self.__player.playerUpdate(self.__input, self.__tileMap, self.__hurtMap)
        self.__tileMap.updateTilemapPosition()
        self.drawGameFrame()
