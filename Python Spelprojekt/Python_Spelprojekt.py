from ast import Pass
import pygame
from sprites import *
from config import *
import sys
class Game:
    
    def __init__(self):
        pygame.init()
        self.font=pygame.font.Font('Python Spelprojekt/comici.ttf',38)
        self.screen=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.clock=pygame.time.Clock()
        
        self.running=True
        self.static=0
        self.intro_background=pygame.image.load('Python Spelprojekt/img/intro_backgr.jpg')
        self.win_bg=pygame.image.load('Python Spelprojekt/img/Win.jpg')
        self.enemy_spritesheet=Spritesheet('Python Spelprojekt/img/Pascal.png')
        self.character_spritesheet=Spritesheet('Python Spelprojekt/img/sprites_base.png')
        self.terrain_spritesheet=Spritesheet('Python Spelprojekt/img/floor_base.png')
        self.fighter_spritesheet=Spritesheet('Python Spelprojekt/img/big_character.png')
        self.wall_spritesheet=Spritesheet('Python Spelprojekt/img/Wall.png')
        self.door_spritesheet=Spritesheet('Python Spelprojekt/img/Door.png')
        self.arena_spritesheet=pygame.image.load('Python Spelprojekt/img/Arena.png')
    def Tilemap(self): #follows the map in config
        for i, row in enumerate(tilemap): #y position
            for j, column in enumerate(row): #x position
                Ground(self,j,i)
                if column=="B":
                    Block(self,j,i)
                
                if column=="1":
                    Door1(self,j,i)
                if column=="2":
                    Door2(self,j,i)
                if column=="3":
                    Door3(self,j,i)
    def TilemapArena(self):
        for i, row in enumerate(tilemap_arena):
            for j, column in enumerate(row):
                if column=="E":
                    Enemy(self,j,i)
                if column=="F":
                   Fighter(self,j,i)


    def new(self):
        #the start of the new game
        self.playing=True

        self.player=pygame.sprite.LayeredUpdates()
        self.blocks=pygame.sprite.LayeredUpdates() #the wallllsss
        self.door1=pygame.sprite.LayeredUpdates()
        self.door2=pygame.sprite.LayeredUpdates()
        self.door3=pygame.sprite.LayeredUpdates()
        self.all_sprites=pygame.sprite.LayeredUpdates()
        self.Tilemap()


    def newArena(self):
        self.playing=True
        
        self.fighter=pygame.sprite.LayeredUpdates()
        self.enemy=pygame.sprite.LayeredUpdates()
        #self.player=pygame.sprite.LayeredUpdates()
        self.all_sprites_arena=pygame.sprite.LayeredUpdates()
        self.TilemapArena()

    
    
    def events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: #checks if window is closed
                self.playing=False
                self.running=False


    

    def update(self): #moves the image
        self.all_sprites.update()
    def updateArena(self):
        self.all_sprites_arena.update()
        
    def check(self):
        if self.static==0:
            self.static+=1
            
            self.newArena()
            
        else:
            pass
        

    def draw(self,wins):
    
        self.screen.fill(BLACK) #creates the background for the winodw
        self.all_sprites.draw(self.screen) #puts everything on the window
        self.clock.tick(FPS) #how many time per second it updates

        won=str(wins)+' out of 3 battles won'
        winning=self.font.render(won,True, WHITE)
        winning_rect=winning.get_rect(x=5,y=5)

        self.screen.blit(winning,winning_rect)
        pygame.display.update() #gives the updated screen

    def drawArena(self,enemyhp,playerhp):
        self.screen.blit(self.arena_spritesheet,(0,0))
        
        self.all_sprites_arena.draw(self.screen)
        self.clock.tick(FPS)
        attack_button=Button(360,290,128,50,WHITE,'Attack',28)
        defend_button=Button(360,350,128,50,WHITE,'Defend',28)
        
        enemy='Enemy HP: '+str(enemyhp)
        player='Player HP: '+str(playerhp)
        enemy_hp=self.font.render(enemy,True, WHITE)
        enemy_hp_rect=enemy_hp.get_rect(x=350,y=10)
        player_hp=self.font.render(player,True, WHITE)
        player_hp_rect=player_hp.get_rect(x=20,y=10)

        self.screen.blit(attack_button.image,attack_button.rect) 
        self.screen.blit(defend_button.image,defend_button.rect)
        self.screen.blit(enemy_hp,enemy_hp_rect)
        self.screen.blit(player_hp,player_hp_rect) 
        pygame.display.update()


    def statemanager(self,level,enemyhp,playerhp,wins):
        
        if level=="intro":
            self.intro_screen()
        if level=="hallway":
            self.hallway(wins)  #skriver antalet wins
        if level=="level1" :
            self.enemy_spritesheet=Spritesheet('Python Spelprojekt/img/Niklas.png')
            self.check()
            self.level1(enemyhp,playerhp)
            
        if level=="level2":
            self.enemy_spritesheet=Spritesheet('Python Spelprojekt/img/Henrik.png')
            self.check()
            
            self.level2(enemyhp,playerhp)
        if level=="level3":
            self.enemy_spritesheet=Spritesheet('Python Spelprojekt/img/Pascal.png')
            self.check()
            
            self.level3(enemyhp,playerhp)
        if level=="you_win":
            self.you_win()

            
    def hallway(self,wins):
        #game loop
        
        self.static=0
        self.events()
        self.draw(wins)
        self.update()

       
    def level1(self,enemyhp,playerhp):
        
        
        self.events()
        self.drawArena(enemyhp,playerhp)
        self.update()
        self.updateArena()
        
        

    def level2(self,enemyhp,playerhp):
        self.events()
        self.drawArena(enemyhp,playerhp)
        self.update()
        self.updateArena()

    def level3(self,enemyhp,playerhp):
        self.events()
        self.drawArena(enemyhp,playerhp)
        self.update()
        self.updateArena()
            
        

    def you_win(self):
        self.events()
        
        title=self.font.render('YOU WIN!!',True, BLACK)
        title_rect=title.get_rect(x=250,y=225)
        self.screen.blit(self.win_bg,(-30,0))
        self.screen.blit(title,title_rect)
        pygame.display.update()

    def intro_screen(self):
        intro=True
        self.running=True
        title=self.font.render('First term Simulator',True, YGR)
        title_rect=title.get_rect(x=150,y=30)
        
        play_button=Button(270,200,128,50,WHITE,'Play',32)
        quit_button=Button(270,300,128,50,WHITE,'QUIT',32)
        while intro:
            for event in pygame.event.get():
                if event.type==pygame.QUIT: #checks if window is closed
                    intro=False
                    self.running=False
            mouse_pos=pygame.mouse.get_pos()
            mouse_pressed=pygame.mouse.get_pressed()
        
            if play_button.is_pressed(mouse_pos,mouse_pressed):
                intro=False 
            if quit_button.is_pressed(mouse_pos,mouse_pressed):
                intro=False
                self.running=False

            self.screen.blit(self.intro_background,(-300,-50))
            self.screen.blit(title,title_rect)
            self.screen.blit(play_button.image,play_button.rect) 
            self.screen.blit(quit_button.image,quit_button.rect) 
            pygame.display.update()
g=Game()

g.intro_screen()
g.new()


p=Player(g,4,6) #skapar objektet player for att dela dess info med game class

while g.running:
    
    g.statemanager(p.level,p.f.enemyhp,p.f.playerhp,p.win)
    
    

pygame.quit()
sys.exit()