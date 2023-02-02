from typing import Tuple
from pygame.math import Vector2
from random import randrange
import time
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

clock = pygame.time.Clock()
pygame.init()


world = pygame.display.set_mode([worldx,worldy])
backdrop = pygame.image.load(os.path.join('images','stage.png'))
backdropbox = world.get_rect()

def findHighScore(scores):
    score = max(scores)
    return score

# Objects
class SnowBall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 1
        self.movey = 0
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join('images', 'snow-0.png')).convert()
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
        #self.movex = randrange(3,5)
        if self.rect.x <= 0:
            self.rect.y = randrange(210,215)
            self.rect.x = 700
            self.movex += 0.5

class IceFall(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.movex = 0
        self.movey = 1
        self.frame = 0
        self.images = []
        img = pygame.image.load(os.path.join('images', 'ice-0.png')).convert()
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

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.frame = 0
        self.pos = 0
        self.spin = 0
        self.images = []
        for i in range(0,15):
            img = pygame.image.load(os.path.join('images', 'coin-' + str(i) + '.png')).convert()
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
            img = pygame.image.load(os.path.join('images', 'p-' + str(i) + '.png')).convert()
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



# Setup
backdrop = pygame.image.load(os.path.join('images', 'stage.png'))
clock = pygame.time.Clock()
pygame.init()
FONT = pygame.font.SysFont("Sans", 30)
backdropbox = world.get_rect()

main = True

player = Player()  # spawn player
player.rect.x = 175  # go to x
player.rect.y = ground  # go to y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 4
walk = 5
jump = 25

IceFall_list = pygame.sprite.Group()
SnowBall_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
Coin_list = pygame.sprite.Group()
entity_list = pygame.sprite.Group()
entity_list.add(player)

ice = IceFall()
ice.rect.x = randrange(30,670)
sb = SnowBall()
sb.rect.y = randrange(210,215)

SnowBall_list.add(sb)
IceFall_list.add(ice)
enemy_list.add(sb)
enemy_list.add(ice)
entity_list.add(ice)
entity_list.add(sb)

coin = Coin()
coin.rect.x = randrange(50,600)
coin.rect.y = randrange(90, 200)
Coin_list.add(coin)

while main:

    # Collison player with Enemy. End Game
    if pygame.sprite.spritecollideany(player, enemy_list):
        dead = True
        HIGHSCORE = findHighScore(SCORES)
        while dead:
            world.fill(RED)
            world.blit(FONT.render('RIP...Final Score: '+str(SCORE), True, WHITE), (235, 160))
            world.blit(FONT.render('Play Again? (y/n)', True, WHITE), (250, 240))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == ord('n') or event.key == ord('q'):
                        for entity in entity_list:
                            entity.kill()
                        pygame.quit()
                        sys.exit()
                    if event.key == ord('y'):
                        dead = False
                        SCORE = 0
                        LVL = 0
                        SCORES.clear()
                        SCORES.append(HIGHSCORE)
                        player.movex = 0
                        player.movey = 0
                        player.rect.x = 175  # go to x
                        player.rect.y = ground  # go to y
                        ice.rect.y = ground + 40
                        ice.movey = 0.5
                        sb.rect.x = 0
                        sb.movex = 1

            world.blit(backdrop, backdropbox)
            world.blit(FONT.render('SCORE: '+str(SCORE), True, WHITE), (300, 20))

    # Collision player with Coin
    elif pygame.sprite.spritecollideany(player, Coin_list):
        SCORE += 1
        SCORES.append(SCORE)
        for c in Coin_list:
            c.kill()
        coin = Coin()
        coin.rect.x = randrange(50,600)
        coin.rect.y = randrange(90, 200)
        Coin_list.add(coin)
        
    for event in pygame.event.get():
        
        
        # User hit 'q' to quit
        if event.type == pygame.QUIT:
            pygame.quit() 
            try: 
                sys.exit()
            finally:
                main = False

        
        if event.type == pygame.KEYDOWN:

            if event.key == ord('q'):
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    main = False
            if event.key == ord('a'):
                player.control(-steps, 0)
            if event.key == ord('d'):
                player.control(steps, 0) 
            #if event.key == pygame.K_SPACE and player.jump == False:
            if event.key == ord('w') or event.key ==  pygame.K_SPACE and player.jump == False:
                player.jump = True
                player.control(0, -jump)

        if event.type == pygame.KEYUP:
            if event.key == ord('a'):
                player.control(steps, 0)
            if event.key == ord('d'):
                player.control(-steps, 0)
    player.rect.clamp_ip(backdropbox)
    world.blit(backdrop, backdropbox)
    world.blit(FONT.render('SCORE: '+str(SCORE), True, WHITE), (300, 20))
    world.blit(FONT.render('HIGH SCORE: '+str(HIGHSCORE), True, WHITE), (500, 20))
    player.gravity()
    player.update()
    coin.update()
    ice.gravity()
    ice.update()
    sb.momentum()
    sb.update()   
    Coin_list.draw(world)
    IceFall_list.draw(world)
    SnowBall_list.draw(world)
    player_list.draw(world)
    entity_list.draw(world)
    pygame.display.flip()
    clock.tick(fps)