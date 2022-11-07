#from logging import _Level
from operator import truediv
import pygame
from config import *
import math
import random
class Spritesheet:
    def __init__(self,file):
        self.sheet=pygame.image.load(file).convert()

    def get_sprite(self,x,y,width,height):
        sprite=pygame.Surface([width,height])
        sprite.blit(self.sheet,(0,0),(x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite

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
        self.animation_loop=1
        self.image=self.game.character_spritesheet.get_sprite(36,-1,self.width,self.height)
        

        self.rect=self.image.get_rect() #Where the player is 'hitbox' etc
        self.rect.x=self.x
        self.rect.y=self.y
        
        self.level="hallway"
        self.win=0
        self.static=0
        self.f=Fight(70,100)
        
        
        

    def update(self):
      
        if self.win==0:
            if pygame.sprite.spritecollide(self,self.game.door1,False):
                
                self.level="level1"
                
                self.check()
                
                if self.f==0:   #if fight is finished player is put back in hallway and a new sequence starts
                
                    self.rect.y=self.y+7

                    self.level="hallway" 
                    if self.win==1:
                        self.f=Fight(100,100) 
                    else:
                        self.f=Fight(70,100)
        else:
            hits=pygame.sprite.spritecollide(self,self.game.door1,False)
            if hits:
                if self.y_change<0:
                    self.rect.y=hits[0].rect.bottom
          
        if self.win==1:
            if pygame.sprite.spritecollide(self,self.game.door2,False):
            
                self.level="level2"
                self.check()
            
                if self.f==0:
            
                    self.rect.y=self.y+7

                    self.level="hallway" 
                    if self.win==2:
                        self.f=Fight(120,100) 
                    else:
                        self.f=Fight(100,100) 
        else:
            hits=pygame.sprite.spritecollide(self,self.game.door1,False)
            if hits:
                if self.y_change<0:
                    self.rect.y=hits[0].rect.bottom
            
                 
        if self.win==2:
            if pygame.sprite.spritecollide(self,self.game.door3,False):
            
                self.level="level3"
                self.check()
            
                if self.f==0 and self.win==2:
            
                    self.rect.y=self.y+7
                    self.level="hallway" 
                    self.f=Fight(120,100) 
                elif self.f==0 and self.win==3:
                    self.f=Fight(120,100) #this fight sequence is started to not get a boolean error
                    self.level="you_win"
        else:
            hits=pygame.sprite.spritecollide(self,self.game.door1,False)
            if hits:
                if self.y_change<0:
                    self.rect.y=hits[0].rect.bottom
        
            
                 
        self.movement()
        self.animate()

        self.rect.x += self.x_change
        self.collide_blocks('x')

        self.rect.y += self.y_change #updates to the new location
        self.collide_blocks('y')

        self.x_change=0 #otherwise it keeps moving
        self.y_change=0
        
            
    
    def check(self): #function checks if the fight is finished
        
        if self.f.status()==False:
            if self.f.Win():
                self.win+=1

            self.f=0
            
        else:
            self.f.fight()
            
        


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
                
                if self.x_change>0:                 #keeps the player from going through the wall
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
    def animate(self):
        down_animations = [self.game.character_spritesheet.get_sprite(36, -1, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(4, -1, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(68, -1, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(36, 31, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(3, 31, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(68, 31, self.width, self.height)]

        right_animations = [ self.game.character_spritesheet.get_sprite(38, 63, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(6, 63, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(70, 63, self.width, self.height)]

        up_animations = [self.game.character_spritesheet.get_sprite(38, 95, self.width, self.height),
            self.game.character_spritesheet.get_sprite(6, 95, self.width, self.height),
                        self.game.character_spritesheet.get_sprite(70, 95, self.width, self.height)]
        if self.facing=="down":
            if self.y_change==0:
                self.image=self.game.character_spritesheet.get_sprite(36,-1,self.width,self.height)
            else:
                self.image=down_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1
        if self.facing=="up":
            if self.y_change==0:
                self.image=self.game.character_spritesheet.get_sprite(38,95,self.width,self.height)
            else:
                self.image=up_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1
        if self.facing=="left":
            if self.x_change==0:
                self.image=self.game.character_spritesheet.get_sprite(36,31,self.width,self.height)
            else:
                self.image=left_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1
        if self.facing=="right":
            if self.x_change==0:
                self.image=self.game.character_spritesheet.get_sprite(38,63,self.width,self.height)
            else:
                self.image=right_animations[math.floor(self.animation_loop)]
                self.animation_loop+=0.1
                if self.animation_loop>=3:
                    self.animation_loop=1
            
class Fight:
    def __init__(self,enemyhp,playerhp):
        self.enemyhp=enemyhp
        self.playerhp=playerhp
        self.computer_choice=0
        self.player_choice=0
        
        self.win=0
    def computerchoice(self):
        if self.enemyhp>0:
            choice=random.choice(range(0,1))
            if choice==0:
                self.computer_choice=0
                self.attack("enemy")
                
                return
            else:
                self.computer_choice=1
                return 
        else:
            self.Win()
    def playerchoice(self):
        if self.playerhp>0:
            rectbut1=pygame.Rect(360,290,128,50)
            rectbut2=pygame.Rect(360,350,128,50)
            for event in pygame.event.get():
                pos=pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN  :
                    if rectbut1.collidepoint( pos):
                        
            
                        self.player_choice=0
                        self.attack("player")
                
                        return True
                    elif rectbut2.collidepoint(pos):
                        self.player_choice=1
                        
                        return True
                    else:
                        return False
                else:
                    return False
                  
        else:
            self.lose()
    def attack(self,attacker):
        chance=random.choice(range(0,100))
        if attacker=="player":
            if chance<=20:
                pass
            elif chance>20:
                if self.computer_choice==1:
                    self.enemyhp-=10*self.defend()
            
                    
                else:
                    self.enemyhp-=10
                
                    
        elif attacker=="enemy":
            if chance<=20:
                pass
            elif chance>20:
                if self.player_choice==1:
                    self.playerhp-=10*self.defend()
            
                    
                else:
                    self.playerhp-=10
                
                    
        
        
    def defend(self):
        chance=random.choice(range(0,100))
        if chance<=15:
            return 0
        elif chance>15 and chance<80:
            return 0.5
        else:
            return 1

    def Win(self):
        if self.enemyhp<=0:
            self.win+=1
            
            return True
        return False
    def lose(self):
        if self.playerhp<=0:
            
            return True
        return False
    def fight(self):
       
        
        if self.playerchoice():
        
            self.computerchoice()
        

    def status(self):
        return not(self.Win() or  self.lose())  #function gets checked by player class to see if the fight has finished
        
        
class Ground(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer=GROUND_LAYER
        self.groups=self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE
        #self.image=pygame.Surface([self.width,self.height])
        #self.image.fill(RED)
        self.image=self.game.terrain_spritesheet.get_sprite(22,34,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    
class Fighter(pygame.sprite.Sprite): #For now just an image with no other functionality
    def  __init__(self,game,x,y):
        self.game=game
        self._layer=FIGHTER_LAYER
        self.groups=self.game.all_sprites_arena, self.game.fighter
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*ARENASIZE
        self.y=y*ARENASIZE
        self.width=ARENASIZE
        self.height=ARENASIZE
        self.image=self.game.fighter_spritesheet.get_sprite(0,0,self.width,self.height)
        

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        


class Enemy(pygame.sprite.Sprite): #see comment on Fighter Class
    def __init__(self,game,x,y):
        self.game=game
        self._layer=ENEMY_LAYER
        self.groups=self.game.all_sprites_arena, self.game.enemy
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*ARENASIZE
        self.y=y*ARENASIZE
        self.width=ARENASIZE
        self.height=ARENASIZE
        
        self.image=self.game.enemy_spritesheet.get_sprite(0,0,self.width,self.height)
        

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

        self.image=self.game.wall_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Door1(pygame.sprite.Sprite): #Creates the doors
    def __init__(self,game,x,y):
        self.game=game
    
        
        self._layer=DOOR_LAYER
        self.groups=self.game.all_sprites,self.game.door1
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE+1

        self.image=self.game.door_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    
class Door2(pygame.sprite.Sprite): #Creates the doors
    
    
    def __init__(self,game,x,y):
        
        self.game=game
        self._layer=DOOR_LAYER
        self.groups=self.game.all_sprites,self.game.door2
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.open=False

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE+1

        self.image=self.game.door_spritesheet.get_sprite(0,0,self.width,self.height)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
class Door3(pygame.sprite.Sprite): #Creates the doors
    
    def __init__(self,game,x,y):
        
        self.game=game
        self._layer=DOOR_LAYER
        self.groups=self.game.all_sprites,self.game.door3
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.open=False
        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE+1
        self.image=self.game.door_spritesheet.get_sprite(0,0,self.width,self.height)
        

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Button:               #To create a button when called upon with its spritesheet best works with a width of 100px and height of 50px
    def __init__(self,x,y,width,height,fg,content,fontsize):
        self.content=content
        self.font=pygame.font.Font('Python Spelprojekt/comici.ttf',fontsize)
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.fg=fg
        
        self.button_spritesheet=Spritesheet('Python Spelprojekt/img/button.png')
        self.image=self.button_spritesheet.get_sprite(0,9,self.width,self.height)
        
        
        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        self.text=self.font.render(self.content,True,self.fg)
        self.text_rect=self.text.get_rect(center=(self.width//2,self.height//2))
        self.image.blit(self.text,self.text_rect) 
    def is_pressed(self,pos,pressed):
        if self.rect.collidepoint(pos):
            if pressed[0]:
                return True
            return False
        return False
