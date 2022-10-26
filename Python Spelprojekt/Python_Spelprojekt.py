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
                if column=="P":
                    Player(self,j,i)
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
    def statemanager(self):
        if self.state=="hallway":
            self.hallway()
        if self.state=="level1":
            self.level1()
    def hallway(self):
        #game loop
        
        while self.playing:
            self.events()
            self.update()
            self.draw()
            

        self.running=False #when the game is over
    def level1(self):
        pygame.quit()
        #while self.player.hp>0:
         #   self.playing=True
          #  self.event()

    def level2(self):
        pass

            
        

    def game_over(self):
        pass
    def intro_screen(self):
        pass

g=Game()
g.intro_screen()
g.new()
while g.running:
    g.statemanager()
    g.game_over()

pygame.quit()
sys.exit()