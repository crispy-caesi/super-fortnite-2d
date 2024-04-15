# ===================== import ===================== #

import pygame
from TileMap import TileMap
from Player import Player
from Input import KeyInput
from PIL import Image, ImageSequence

from MusicController import MusicController


# ===================== Main ===================== #

class Game():
    """
    Class that fuses all of the subparts together for the game to be playable.
    """

    def __init__(self, __screenResolution, __currentLevel, __background, __currentCharacterSkin, __death_path, __jump_path):
        pygame.mixer.pre_init(44100,16,3,4096)
        pygame.init()
        self.__screenResolution = __screenResolution
        self.__tileMap = TileMap(__currentLevel)
        self.__hurtMap = self.__tileMap.getHurtMap()
        
        images = self.loadGIF(__currentCharacterSkin)
        deathImages=self.loadGIF(__death_path)
        jumpImgages = self.loadGIF(__jump_path)
        self.__player = Player(images=images, deathImages= deathImages, jumpImages= jumpImgages)
        self.__allSprites = pygame.sprite.Group()
        self.__allSprites.add(self.__tileMap)

        self.__allSprites.add(self.__player)
        self.__allSprites.add(self.__player.verticalCollisionBox)
        self.__allSprites.add(self.__player.horizontalCollisionBox)
        self.__background = pygame.image.load(__background).convert()
        self.__background = pygame.transform.scale(self.__background,(self.__screenResolution))
        self.__keyInput = KeyInput()
        self.__clock = pygame.time.Clock()

    def running(self, __screen):
        """
        Method to run the game.
        """
        
        __running = True
        __mcc = MusicController()
        __mcc.initInGameBackgroundMusic("sprites/placeholder/soundsAndMusic/inGameBackgroundMusic.wav")
        __mcc.playInGameBackgroundMusic()


        while __running:
            # input update
            self.__keyInput.getInput()
            # condition to end the running process
            if self.__keyInput.keyescape or self.__player.getIsDead():
                self.__keyInput.keyescape = False
                __running = False

            self.frameUpdate(self.__keyInput, __screen)
            
            self.__clock.tick(120)

        self.resetHurtmap()
        # after the loop is done, return to main menu
        __mcc.stopInGameBackgroundMusic()

    def resetHurtmap(self):
        """
        Method to reset the hurtmap.
        """
        
        self.__hurtMap = None

    def drawGameFrame(self):
        """
        Method to blit the game on the screen.
        """
                
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

    def loadGIF(self,filename):
        """
        Extracting the individual frames from the GIF and storing them in a list
        """
        pilImage = Image.open(filename)
        frames = []
        for frame in ImageSequence.Iterator(pilImage):
            frame = frame.convert('RGBA')
            pygameImage = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode).convert_alpha()
            frames.append(pygameImage)
        return frames

# ============== game loop ============== #

    def frameUpdate(self, __input, __screen):
        """
        Method that lets the game update.
        """

        # runs all of Game.py main functions
        self.__screen = __screen
        self.__keyInput = __input
        self.__player.playerUpdate(self.__keyInput, self.__tileMap, self.__hurtMap)
        self.__tileMap.updateTilemapPosition()
        self.drawGameFrame()

