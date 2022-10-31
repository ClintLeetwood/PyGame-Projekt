#from logging import _Level
import pygame
from config import *
import math
import random
class Player(pygame.sprite.Sprite):
    def __init__(self,game,x,y): #x,y gives the location of the player 
        self.game=game
        self._layer=PLAYER_LAYER #so the player is not under anything
        self.groups=self.game.all_sprites, self.game.player
        pygame.sprite.Sprite.__init__(self,self.groups)#adds player too all sprites
        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.x_change=0
        self.y_change=0
        self.facing='down'

        self.image=pygame.Surface([self.width,self.height])#right now the player is sqaure fill in pic later
        self.image.fill(RED)

        self.rect=self.image.get_rect() #Where the player is 'hitbox' etc
        self.rect.x=self.x
        self.rect.y=self.y
        self.level="hallway"

    def update(self):
        if pygame.sprite.spritecollide(self,self.game.doors,False):
            
            #obj=Game()
            
            
            self.level="level1"
            #g.statemanager("lev)
            return 
          
        self.movement()

        self.rect.x += self.x_change
        self.collide_blocks('x')

        self.rect.y += self.y_change #updates to the new location
        self.collide_blocks('y')

        self.x_change=0 #otherwise it keeps moving
        self.y_change=0
        
            

    def health(self):
        self.hp=100
        hit=pygame.sprite.damage(self,self.game.damage,False)
        if hit:
            self.hp-=self.damage



    def movement(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_change-=PLAYER_SPEED #amount of pixels moved
            self.facing='left'          #maybe unnecessary depending on looks
        if keys[pygame.K_RIGHT]:
            self.x_change+=PLAYER_SPEED 
            self.facing='right'
        if keys[pygame.K_UP]:
            self.y_change-=PLAYER_SPEED 
            self.facing='up'
        if keys[pygame.K_DOWN]:
            self.y_change+=PLAYER_SPEED 
            self.facing='down'
    
    def collide_blocks(self,direction):
        if direction=="x":
            hits= pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                
                if self.x_change>0:
                    self.rect.x=hits[0].rect.left-self.rect.width
                if self.x_change<0:
                    self.rect.x=hits[0].rect.right
        if direction=="y":
            
            hits=pygame.sprite.spritecollide(self,self.game.blocks,False)
            if hits:
                
                if self.y_change>0:
                    self.rect.y=hits[0].rect.top - self.rect.height
                if self.y_change<0:
                    self.rect.y=hits[0].rect.bottom
    
    
        
        
    


                


class Enemy(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer=BLOCK_LAYER
        self.groups=self.game.all_sprites, self.game.enemy
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(BLUE)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y


class Block(pygame.sprite.Sprite): #creates the walls
    def __init__(self,game,x,y):

        self.game=game
        self._layer=BLOCK_LAYER
        self.groups=self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(BLUE)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Door1(pygame.sprite.Sprite): #Creates the doors
    def __init__(self,game,x,y):
        self.game=game
    
        
        self._layer=DOOR_LAYER
        self.groups=self.game.all_sprites,self.game.doors
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(BROWN)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    def open(self):

        self.open=True
class Door2(pygame.sprite.Sprite): #Creates the doors
    def __init__(self,game,x,y):
        self.open=False
        self.game=game
        self._layer=DOOR_LAYER
        self.groups=self.game.all_sprites,self.game.doors
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(BLACK)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
class Door3(pygame.sprite.Sprite): #Creates the doors
    def __init__(self,game,x,y):
        self.open=False
        self.game=game
        self._layer=DOOR_LAYER
        self.groups=self.game.all_sprites,self.game.doors
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE

        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(RED)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
