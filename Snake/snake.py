import math
import random
import pygame
from pygame import mixer
from enum import Enum

#I've implemented:
    # Forbid 180 degree turns 
    # Scoreboard
    # Ending Screen
    # Advanced Scoreboard 
    # Use images instead of figures

# press M for muting

#Note since ive implemented collision method myself and i dont use builtin function, sometimes icon proportions make it look
#collision but its not, as a collision i set the 20 distance between objects more wasn't possible, since blocks are 
# away of 20 units itself.
pygame.init()
fontInit = pygame.font.SysFont("arial",25)
class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    UP = 2
    DOWN = 3
class Volume(Enum):
    MUTED = 0
    UNMUTED = 1

class App:
    
    CubeSize = 20
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
        back = pygame.image.load('background.jpg')
        self.background = pygame.transform.scale(back,(1200,700))
        self.screen = pygame.display.set_mode((1200, 700))
        
       
        
        pygame.display.set_caption("Snake-Game")
        self.clock = pygame.time.Clock()
        self.running = True

        self.width = 1200
        self.height = 700
        self.direction = Direction.RIGHT
        self.head = (self.width//2 , self.height//2)
        self.snake = [self.head,
        (self.head[0] - self.CubeSize,self.head[1]),
        (self.head[0] - (2*self.CubeSize),self.head[1]),
        (self.head[0] - (3*self.CubeSize),self.head[1]),
        (self.head[0] - (4*self.CubeSize),self.head[1])]
        self.score = 0
        self.borders = (0,100)
        self.generateFood()
        self.foodImg = pygame.image.load("apple.png")
        self.snakeImg = pygame.image.load("scared.png")

        self.superFood = None
        self.luckyNumber = 13
        self.printSuperFood = False
        self.superFoodImg = pygame.image.load("hamburger.png")

        self.eatSound = mixer.Sound("Sui.wav")
        self.superFoodSound = mixer.Sound("SuperFood.wav")
       

        #load background music 
        mixer.music.load("sound.wav")
        mixer.music.play(-1)

        self.unmuted = pygame.image.load("unmuted.png")
        self.muted = pygame.image.load("muted.png")
        self.volume = Volume.UNMUTED

    def update(self):
        self.events()
        
        # generating special food with randint
        if random.randint(0,350) == self.luckyNumber and self.printSuperFood == False:
            self.generateSuperFood()
            self.printSuperFood = True
        
        # increment and let system create special food only after it has been eaten
        if self.printSuperFood and self.superFoodCollision():
            self.score += 10
            self.superFoodSound
            self.printSuperFood = False
            if self.volume == Volume.UNMUTED:
                self.superFoodSound.play()

               
        # increment snake body and score after normal food collision
        if self.foodCollisionToSnake():
            self.score += 1
            self.snake.append((self.head[0] - ((len(self.snake)-1)*self.CubeSize),self.head[1]))
            self.generateFood()
            if self.volume == Volume.UNMUTED:
                self.eatSound.play()
        else:
            self.snake.pop()

        self.move(self.direction)
        self.snake.insert(0,self.head) 
        
        if self.collision():
            self.running = False
            if self.volume == Volume.UNMUTED:
                mixer.music.load("death.wav")    
                mixer.music.play()

        

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                
                if event.key ==pygame.K_m:
                    if self.volume == Volume.MUTED:
                        mixer.music.load("sound.wav")
                        mixer.music.play(-1)
                        self.volume = Volume.UNMUTED
                    else:
                        mixer.music.stop()
                        self.volume = Volume.MUTED

                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    if self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.direction != Direction.UP:
                        self.direction = Direction.DOWN   
                
    def render(self):
        self.screen.blit(self.background,(0,0))
        self.clock.tick(15)

        if self.volume == Volume.UNMUTED:
            self.screen.blit(self.unmuted,(1000,10))
        elif self.volume == Volume.MUTED:
            self.screen.blit(self.muted,(1000,10)) 
        
        counter = 0
        for block in self.snake:
            # snakehead printed once
            if counter == 0:
                self.screen.blit(self.snakeImg,(self.head[0],self.head[1]))
                counter += 1
            # printing tale
            else:
                pygame.draw.rect(self.screen,(0,255,0),pygame.Rect(block[0],block[1],self.CubeSize,self.CubeSize))
                pygame.draw.rect(self.screen,(51,51,255),pygame.Rect(block[0]+4,block[1]+4,12,12))

        # printing food and upper border
        self.screen.blit(self.foodImg,(self.food[0],self.food[1]))
        pygame.draw.rect(self.screen, (100,100,100), pygame.Rect(self.borders[0],self.borders[1],1200,8))

        if self.printSuperFood:
            self.screen.blit(self.superFoodImg,(self.superFood[0],self.superFood[1]))
           

        printScore = fontInit.render("Score: " + str(self.score),True,(255,255,255))
        self.screen.blit(printScore,[0,0])   
        
        pygame.display.flip()

    def cleanUp(self):
        self.eatSound.stop()
        self.superFoodSound.stop()
        self.saveScore()
        self.screen.fill((100,100,100))
        printEnding = fontInit.render("Press Q for Quit, Press space for Restart",True,(255,255,255))
        self.screen.blit(printEnding,[400,300])

        topScores = self.topResults()
        printTopScores = fontInit.render(topScores,True,(255,255,255))
        self.screen.blit(printTopScores,[0,0])

        currentScore = fontInit.render("Your Score: " + str(self.score), True,(255,255,255))
        self.screen.blit(currentScore,[0,50])
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
            
      

    def topResults(self):
        file = open("savePoints.txt",'r')
        lines = file.readlines()
        scores = ",".join(lines).replace("\n","")
        return "Top Scores: "+ scores

    def saveScore(self):
        file = open("savePoints.txt",'r')
        lines = file.readlines()
        file.close()
        topScores = "".join(lines).split("\n")
            #pop the last empty space on line 11
        topScores.pop()
        topScores = list(map(lambda x: int(x),topScores))
        
        # 10 line represents top 10
        if len(lines) < 10:
           
           #if dont have 10 number append any result
            file = open("savePoints.txt",'w')
            topScores.append(self.score)
            strScores = list(map(lambda x: str(x) + "\n",sorted(topScores)))
            file.writelines(strScores)
            file.close()

        else:
            #if we have 10 numbers already read it sort its integers, compare to currents core
            #and if its higher then write new top 10
            file = open("savePoints.txt",'w')
            topScores.sort()
            if self.score > topScores[0]:
                topScores[0] = self.score    
            strScores = list(map(lambda x: str(x) + "\n",sorted(topScores)))
            file.writelines(strScores)  
            file.close()              

    def generateFood(self):
        x = random.randint(0,(self.width-self.CubeSize))
        y = random.randint(self.borders[1] + self.CubeSize//2,(self.height-self.CubeSize))
        self.food = (x,y)
       

    def generateSuperFood(self):
        x = random.randint(0,(self.width-self.CubeSize))
        y = random.randint(self.borders[1] + self.CubeSize//2,(self.height-self.CubeSize))
        self.superFood = (x,y)

    # position change accordint to direction 
    def move(self, direction):
        x = self.head[0]
        y = self.head[1]
        if direction == Direction.RIGHT:
            x += self.CubeSize
        elif direction == Direction.LEFT:
            x -= self.CubeSize
        elif direction == Direction.DOWN:
            y += self.CubeSize
        elif direction == Direction.UP:
            y -= self.CubeSize
        self.head = (x,y) 

    # collision of above,left, right screen + upper border + itself
    def collision(self):
        if(self.head[1] <= self.borders[1]):
            return True
        if self.head[0] > self.width - self.CubeSize or self.head[0] < 0 or self.head[1] > self.height-self.borders[0] - self.CubeSize or self.head[1] < 0:
            return True
        for block in self.snake[1:]:
            if self.collisionAux(self.head[0],self.head[1],block[0],block[1]):
                return True
        return False

    def foodCollisionToSnake(self):
        return self.collisionAux(self.head[0],self.head[1],self.food[0],self.food[1])

    def superFoodCollision(self):
        return self.collisionAux(self.head[0],self.head[1],self.superFood[0],self.superFood[1])
    
    # calculates avarage distance between objects and returns collision
    def collisionAux(self,x,y,x1,y1):
        if math.sqrt(math.pow(x - x1,2) + math.pow(y - y1,2)) < 20 :
          return True
        return False
if __name__ == "__main__":
    app = App()
    app.run()