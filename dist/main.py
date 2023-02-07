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
import Characters.characters
import dist.vars

clock = pygame.time.Clock()
pygame.init()

world = pygame.display.set_mode([dist.vars.worldx,dist.vars.worldy])
backdrop = pygame.image.load(os.path.join('images/Stages','main-stage.png'))
backdropbox = world.get_rect()

def findHighScore(scores):
    score = max(scores)
    return score

# Setup
backdrop = pygame.image.load(os.path.join('images/Stages', 'main-stage.png'))
clock = pygame.time.Clock()
pygame.init()
FONT = pygame.font.SysFont("Sans", 30)
backdropbox = world.get_rect()

main = True

player = Characters.characters.Player()  # spawn player
player.rect.x = 175  # go to x
player.rect.y = dist.vars.ground  # go to y
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

ice = Characters.characters.IceFall()
ice.rect.x = randrange(30,670)
sb = Characters.characters.SnowBall()
sb.rect.y = randrange(210,215)

SnowBall_list.add(sb)
IceFall_list.add(ice)
enemy_list.add(sb)
enemy_list.add(ice)
entity_list.add(ice)
entity_list.add(sb)

coin = Characters.characters.Coin()
coin.rect.x = randrange(50,600)
coin.rect.y = randrange(90, 200)
Coin_list.add(coin)

while main:

    # Collison player with Enemy. End Game
    if pygame.sprite.spritecollideany(player, enemy_list):
        dead = True
        dist.vars.HIGHSCORE = findHighScore(dist.vars.SCORES)
        while dead:
            world.fill(dist.vars.RED)
            world.blit(FONT.render('RIP...Final Score: '+str(dist.vars.SCORE), True, dist.vars.WHITE), (235, 160))
            world.blit(FONT.render('Play Again? (y/n)', True, dist.vars.WHITE), (250, 240))
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
                        dist.vars.SCORE = 0
                        dist.vars.LVL = 0
                        dist.vars.SCORES.clear()
                        dist.vars.SCORES.append(dist.vars.HIGHSCORE)
                        player.movex = 0
                        player.movey = 0
                        player.rect.x = 175  # go to x
                        player.rect.y = dist.vars.ground  # go to y
                        ice.rect.y = dist.vars.ground + 40
                        ice.movey = 0.5
                        sb.rect.x = 0
                        sb.movex = 1

            world.blit(backdrop, backdropbox)
            world.blit(FONT.render('SCORE: '+str(dist.vars.SCORE), True, dist.vars.WHITE), (300, 20))

    # Collision player with Coin
    elif pygame.sprite.spritecollideany(player, Coin_list):
        dist.vars.SCORE += 1
        dist.vars.SCORES.append(dist.vars.SCORE)
        for c in Coin_list:
            c.kill()
        coin = Characters.characters.Coin()
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
    world.blit(FONT.render('SCORE: '+str(dist.vars.SCORE), True, dist.vars.WHITE), (300, 20))
    world.blit(FONT.render('HIGH SCORE: '+str(dist.vars.HIGHSCORE), True, dist.vars.WHITE), (450, 20))
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
    clock.tick(dist.vars.fps)