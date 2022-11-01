from ast import Pass
import pygame
from sprites import *
from config import *
import sys
class Game:
    
    def __init__(self):
        pygame.init()
        self.font=pygame.font.Font('Python Spelprojekt/comici.ttf',20)
        self.screen=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.clock=pygame.time.Clock()
        #self.font=pygame.font.Font('Arial',32)
        self.running=True
        self.static=0
        self.intro_background=pygame.Surface((WIN_WIDTH,WIN_HEIGHT))
    def Tilemap(self): #follows the map in config
        for i, row in enumerate(tilemap): #y position
            for j, column in enumerate(row): #x position
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
        #self.all_sprites.remove(self.screen)
        self.fighter=pygame.sprite.LayeredUpdates()
        self.enemy=pygame.sprite.LayeredUpdates()
        self.player=pygame.sprite.LayeredUpdates()
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
        

    def draw(self):
    
        self.screen.fill(BLACK) #creates the background for the winodw
        self.all_sprites.draw(self.screen) #puts everything on the window
        self.clock.tick(FPS) #how many time per second it updates
    
        pygame.display.update() #gives the updated screen
    def drawArena(self):
        
        
        self.screen.fill(BLACK)
        self.all_sprites_arena.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def statemanager(self,level):
        
        if level=="intro":
            self.intro_screen()
        if level=="hallway":
            self.hallway()
        if level=="level1" :
            self.check()
            self.level1()
        if level=="level2":
            self.check()
            self.level2()
        if level=="level3":
            self.check()
            self.level3()

            
    def hallway(self):
        #game loop
        #self.new()
        
            self.events()
            self.draw()
            self.update()

       # print(self.state)
            

            

        #self.running=False #when the game is over
    def level1(self):
    
        
        self.events()
        self.drawArena()
        self.update()
        self.updateArena()
        

    def level2(self):
        self.events()
        self.drawArena()
        self.updateArena()
    def level3(self):
        self.events()
        self.drawArena()
        self.updateArena()
            
        

    def you_win(self):
        pass

    def intro_screen(self):
        intro=True
        self.running=True
        title=self.font.render('First term Simulator',True, WHITE)
        title_rect=title.get_rect(x=220,y=30)
        
        play_button=Button(270,200,100,50,BLUE,WHITE,'Play',32)
        quit_button=Button(270,300,100,50,BLUE,WHITE,'QUIT',32)
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

            self.screen.blit(self.intro_background,(0,0))
            self.screen.blit(title,title_rect)
            self.screen.blit(play_button.image,play_button.rect) 
            self.screen.blit(quit_button.image,quit_button.rect) 
            pygame.display.update()
g=Game()
g.intro_screen()
g.new()


p=Player(g,4,6) #skapar objektet

while g.running:
    
    g.statemanager(p.level)
    

pygame.quit()
sys.exit()