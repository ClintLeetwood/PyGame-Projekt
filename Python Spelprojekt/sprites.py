#from logging import _Level
from operator import truediv
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
        self.win=0
        self.static=0
        self.f=Fight(70,100)
        
        
        

    def update(self):
      
        if self.win==0:
            if pygame.sprite.spritecollide(self,self.game.door1,False):
                
                self.level="level1"
                
                self.check()
                
                if self.f==0:
                
                    self.rect.y=self.y+7

                    self.level="hallway" 
                    if self.win==1:
                        self.f=Fight(100,100) 
                    else:
                        self.f=Fight(70,100)
        
          
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
        
            
                 
        if self.win==2:
            if pygame.sprite.spritecollide(self,self.game.door3,False):
            
                self.level="level3"
                self.check()
            
                if self.f==0 and self.win==2:
            
                    
                    self.rect.y=self.y+7
                    self.level="hallway" 
                    self.f=Fight(120,100) 
                elif self.f==0 and self.win==3:
                    
                    self.level="you_win"
        
        
            
                 
        self.movement()

        self.rect.x += self.x_change
        self.collide_blocks('x')

        self.rect.y += self.y_change #updates to the new location
        self.collide_blocks('y')

        self.x_change=0 #otherwise it keeps moving
        self.y_change=0
        
            
    
    def check(self):
        
        if self.f.status()==False:
            if self.f.Win():
                self.win+=1

            self.f=0
            print(self.win)
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
            rectbut1=(305,200,100,50)
            rectbut2=(305,300,100,50)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos(rectbut1):

            
                    self.player_choice=0
                    self.attack("player")
                
                    return True
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pos(rectbut2):
                    self.player_choice=1
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
            print("enemy ",self.enemyhp, "player ",self.playerhp)
        
            

    def status(self):
        return not(self.Win() or  self.lose())
        
        

    



    
        
        
class Fighter(pygame.sprite.Sprite):
    def  __init__(self,game,x,y):
        self.game=game
        self._layer=FIGHTER_LAYER
        self.groups=self.game.all_sprites_arena, self.game.fighter
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*ARENASIZE
        self.y=y*ARENASIZE
        self.width=ARENASIZE
        self.height=ARENASIZE

        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(RED)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
        
    


                


class Enemy(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        self.game=game
        self._layer=ENEMY_LAYER
        self.groups=self.game.all_sprites_arena, self.game.enemy
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*ARENASIZE
        self.y=y*ARENASIZE
        self.width=ARENASIZE
        self.height=ARENASIZE

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
        self.groups=self.game.all_sprites,self.game.door1
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.x=x*TILESIZE
        self.y=y*TILESIZE
        self.width=TILESIZE
        self.height=TILESIZE+1

        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(BROWN)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y
    def open(self):

        self.open=True
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

        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(BLACK)

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

        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(RED)

        self.rect=self.image.get_rect()
        self.rect.x=self.x
        self.rect.y=self.y

class Button:
    def __init__(self,x,y,width,height,fg,bg,content,fontsize):
        self.content=content
        self.font=pygame.font.Font('Python Spelprojekt/comici.ttf',fontsize)
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.fg=fg
        self.bg=bg

        self.image=pygame.Surface([self.width,self.height])
        self.image.fill(self.bg)
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
