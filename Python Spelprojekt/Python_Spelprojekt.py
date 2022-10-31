import pygame
from sprites import *
from config import *
import sys
class Game:
    def __init__(self):
        pygame.init()
        self.state="hallway"
        self.screen=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.clock=pygame.time.Clock()
        #self.font=pygame.font.Font('Arial',32)
        self.running=True

    def Tilemap(self): #follows the map in config
        for i, row in enumerate(tilemap): #y position
            for j, column in enumerate(row): #x position
                if column=="B":
                    Block(self,j,i)
                #if column=="P":
                   # Player(self,j,i)
                if column=="1":
                    Door1(self,j,i)
                if column=="2":
                    Door2(self,j,i)
                if column=="3":
                    Door3(self,j,i)


    def new(self):
        #the start of the new game
        self.playing=True

        self.player=pygame.sprite.LayeredUpdates()
        self.blocks=pygame.sprite.LayeredUpdates() #the wallllsss
        self.doors=pygame.sprite.LayeredUpdates()
        self.all_sprites=pygame.sprite.LayeredUpdates()
        self.Tilemap()

    def resetstate(self):
        self.playing=True
        self.player= pygame.sprite.remove()

        self.all_sprites.empty()
    
    def events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT: #checks if window is closed
                self.playing=False
                self.running=False


    def open_door(self):
        #self.doors=
        pass

    def update(self): #moves the image
        self.all_sprites.update()

    def draw(self):
    
        self.screen.fill(BLACK) #creates the background for the winodw
        self.all_sprites.draw(self.screen) #puts everything on the window
        self.clock.tick(FPS) #how many time per second it updates
    
        pygame.display.update() #gives the updated screen
    def drawArena(self):
        self.screen.fill(BLUE)
        self.clock.tick(FPS)

    def statemanager(self,level):
        
        if level=="intro":
            self.intro_screen()
        if level=="hallway":
            self.hallway()
        if level=="level1" :
            self.level1()
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
        self.screen.fill(BLUE)
        self.all_sprites.remove(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
        
        #while self.player.hp>0:
         #   self.playing=True
          #  self.event()

    def level2(self):
        pass

            
        

    def game_over(self):
        pass
    def intro_screen(self):
        
        self.events()   
        self.screen.fill(RED)
        self.update()
        pygame.display.update()
g=Game()

g.new()

p=Player(g,4,6) #skapar objektet
while g.running:
    
    
    g.statemanager(p.level)
    
   

    

pygame.quit()
sys.exit()