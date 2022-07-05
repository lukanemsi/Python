import math
import random
import pygame
from pygame import mixer
from enum import Enum

# Better Visual
# Menu
# Ending
# Audio
# Infinite Game
pygame.init()
fontInit = pygame.font.SysFont("arial",25)

class Valume(Enum):
    MUTED = 0
    UNMUTED = 1

class App:

    GRAVITY = 3
    MOVINGFORCE = 4
    def __init__(self):
        self.running = False
        self.clock = None
        self.screen = None

    def run(self):
        self.init()
        while self.running:
            self.update()
            self.render()
        self.cleanUp()

    def init(self):
        self.screen = pygame.display.set_mode((1200, 700))
        self.height = 700
        self.length = 1200
        pygame.display.set_caption("Flappy-Bird")

        self.clock = pygame.time.Clock()      
        self.score = 0      
        self.running = True
        background = pygame.image.load("background.jpg")
        self.background = pygame.transform.scale(background,(1200,700))
        self.moveScreen = 0
        
        self.border = (0,100)

        self.birdImg = pygame.image.load("bird1.png")
        self.birdCordinate = (self.length / 50 ,self.height / 2)


 
        self.pipeSize = [80,200]
        self.pipe = (1100,-200)
        self.riversePipe = (1100,500)
        

        mixer.music.load("song.wav")
        mixer.music.play(-1)

        self.unmuted = pygame.image.load("unmuted.png")
        self.muted = pygame.image.load("muted.png")
        self.coin = pygame.image.load("bitcoin.png")
        self.coinCordinates = [1100,400]
        self.coinCollision = False
        self.coinSound = mixer.Sound("coinSound.wav")
        self.valume = Valume.UNMUTED
        
    def update(self):
        self.events()
        self.changeBirdPosition()
        self.changeCoinPosition()
        self.pipe = self.changePipePosition(self.pipe)
        self.riversePipe = self.changePipePosition(self.riversePipe)
        
        if self.collisionToCoin():
            self.coinCollision = True
            self.score += 10
            if self.valume == Valume.UNMUTED:
                self.coinSound.play()
            self.changeCoinPosition()
        
        if self.pipe[0] < -100:
            self.appearPipesAgain()
        if self.collision():
            self.running = False
        if self.collisionToPipe():
            self.running = False

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_m:
                    if self.valume == Valume.MUTED:
                        mixer.music.unpause()
                        self.valume = Valume.UNMUTED
                    else:
                        mixer.music.pause()
                        self.coinSound.stop()
                        self.valume = Valume.MUTED

                if event.key == pygame.K_SPACE:
                    self.changeBirdPosition()
                    self.GRAVITY = -6
            elif pygame.mouse.get_pressed()[0]:
                    self.changeBirdPosition()
                    self.GRAVITY = -6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.GRAVITY = 3
            elif event.type == pygame.MOUSEBUTTONUP:
                self.GRAVITY = 3
                

    def render(self):
        self.clock.tick(100)
        
        self.screen.blit(self.background,(0,0))
        self.screen.blit(self.birdImg,self.birdCordinate)
        
        pygame.draw.rect(self.screen, (225,225,225), pygame.Rect(self.border[0],self.border[1],1200,8))

        pygame.draw.rect(self.screen, (211,253,117), pygame.Rect(self.pipe[0],self.pipe[1],80,500))
        pygame.draw.rect(self.screen, (211,253,117), pygame.Rect(self.riversePipe[0],self.riversePipe[1],80,500))

        if self.valume == Valume.UNMUTED:
            self.screen.blit(self.unmuted,(1000,10))
        elif self.valume == Valume.MUTED:
            self.screen.blit(self.muted,(1000,10))

        self.screen.blit(self.coin,self.coinCordinates)
        printScore = fontInit.render("Score: " + str(self.score),True,(255,255,255))
        printName =  fontInit.render("Angry Bird",True,(255,255,255))
        self.screen.blit(printScore,[0,0])
        self.screen.blit(printName,[200,0])

        pygame.display.flip()


    def cleanUp(self):
        self.coinSound.stop()
        if self.valume == Valume.UNMUTED:
            mixer.music.load("collisionSound.wav")    
            mixer.music.play()
        self.screen.fill((100,100,100))
        finalScore = fontInit.render("Score: " + str(self.score),True,(255,255,255))
        self.screen.blit(finalScore,[0,0])
        printEnding = fontInit.render("Press Q for Quit, Press space for Restart",True,(255,255,255))
        self.screen.blit(printEnding,[400,300])
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if  event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q :
                        quit()
                    elif event.key == pygame.K_SPACE:
                        self.run()


    
    def changeBirdPosition(self):
        (x,y) = self.birdCordinate 
        y += self.GRAVITY
        self.birdCordinate = (x,y)


    def changePipePosition(self,pipe):
        (x,y) = pipe
        x -= self.MOVINGFORCE
        return (x,y) 
 
    def changeCoinPosition(self):
        if self.coinCordinates[0] < -50 or self.coinCollision:
            x = random.randint(100,1100)
            y = random.randint(150,650)
            self.coinCordinates = [x,y]
            self.coinCollision = False
        else:
            self.coinCordinates[0] -= self.MOVINGFORCE

    def appearPipesAgain(self):    
            rand = random.randint(-360,-50)
            self.pipe = (1100,rand) 
            self.riversePipe = (1100,rand + 700)

    def collisionToPipe(self):
        if self.birdCordinate[0] == self.pipe[0]:
            if self.pipe[1] + 500 >= self.birdCordinate[1] or self.riversePipe[1] - 70 <= self.birdCordinate[1]:
                return True
            else:
                self.score += 1
        return False



    def collision(self):
        if self.birdCordinate[1] <= self.border[1]:
            return True
        if  self.birdCordinate[1] >= self.height - 20:    
            return True
        return False

    def collisionToCoin(self):
       return self.collisionAux(self.birdCordinate[0],self.birdCordinate[1],self.coinCordinates[0],self.coinCordinates[1])

    def collisionAux(self,x,y,x1,y1):
        if math.sqrt(math.pow((x - x1),2) + math.pow((y - y1),2)) < 40 :
          return True
        return False

if __name__ == "__main__":
    app = App()
    app.run()