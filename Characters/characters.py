from random import randrange
# Load pygame keywords
import pygame
# Let python use file system
import sys
# Help python identify OS
import os

# Variables
worldx = 700
worldy = 400
ground = 225
fps = 60
ani = 4
BLUE = (25, 25, 200)
BLACK = (23,23,23)
WHITE = (254,254,254)
RED = (136, 8, 8)
ALPHA = (0, 0, 0)
SCORE = 0
SCORES = [0]
HIGHSCORE = 0
LVL = 0


#---------Snowball Enemy-------------#
class SnowBall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 1
        self.movey = 0
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join('images/Snowball', 'snow-0.png')).convert()
        img.convert_alpha()
        img.set_colorkey(ALPHA)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def update(self):
        # Update sprite position
        self.rect.x = self.rect.x - self.movex
        self.rect.y = self.rect.y - self.movey

    def momentum(self):
        self.frame += 1
        if self.rect.x <= 0:
            self.rect.y = randrange(210,215)
            self.rect.x = 700
            self.movex += 0.5


#------------Ice Enemy-------------#
class IceFall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 1
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join('images/Ice', 'ice-0.png')).convert()
        img.convert_alpha()
        img.set_colorkey(ALPHA)
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def update(self):
        # Update sprite position
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey

    def gravity(self):
        self.frame += 1
        #self.movey = randrange(1,5)
        if self.rect.y >= ground + 40:
            self.rect.y = 0
            self.rect.x = randrange(10,680)
            self.movey += 0.5

#---------Coin Sprite-------------#
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.pos = 0
        self.spin = 0
        self.images = []
        for i in range(0,15):
            img = pygame.image.load(os.path.join('images/Coin', 'coin-' + str(i) + '.png')).convert()
            img.convert_alpha() #optimize alpha
            img.set_colorkey(ALPHA) # set alpha
            self.images.append(img)
            self.image = self.images[0]
            self.rect =  self.image.get_rect()

    def update(self):
        if self.spin == 1:
            self.spin = 0
            self.frame += 1
            if self.frame > 15:
                self.frame = 0
            self.image = self.images[self.frame//ani]
        else:
            self.spin += 1


#--------------Player-------------#
class Player(pygame.sprite.Sprite):
    # Spawn a player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.jumpCount = 0
        self.jump = False
        self.isDoubleJump = False
        self.images = []
        for i in range(0, 7):
            img = pygame.image.load(os.path.join('images/Player', 'p-' + str(i) + '.png')).convert()
            img.convert_alpha() #optimize alpha
            img.set_colorkey(ALPHA) # set alpha
            self.images.append(img)
            self.image = self.images[0]
            self.rect =  self.image.get_rect()
            

    def gravity(self):
        if self.rect.y > ground and self.movey >= 0:
            self.movey = 0
            self.rect.y = ground
        self.movey += 2

    def control(self, x, y):
        # Control player movement
        self.movex += x
        self.movey += y-0.5

    def update(self):
        # Update sprite position
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame // ani], True, False)

        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3*ani:
                self.frame = 0
            self.image = self.images[self.frame//ani]
        
        # jumping
        if self.jump == True:
            if(self.jumpCount == 2):
                self.isDoubleJump = True
                self.jump = False
            self.jumpCount += 1
        if self.rect.y >= ground:
            self.jump = False
            self.isDoubleJump = False
            self.jumpCount = 0