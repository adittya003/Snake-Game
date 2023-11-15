import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
class Direction(Enum):
    RIGHT=1
    LEFT=2
    UP=3
    DOWN=4


Point = namedtuple('Point','x, y')
BLOCK_SIZE=20
FPS=100
#rgb
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE1=(0,0,255)
RED=(255,0,0)
BLUE2=(0,100,255)
PURPLE = (150, 0, 150)

pygame.init()
font= pygame.font.Font('arial.ttf',32)


class SnakeGameAI:
    def __init__(self,width=600,height=400):

        self.width=width
        self.height=height

        #init_game display
        self.display=pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Snake Game")
        self.clock=pygame.time.Clock()

        #init game state
        self.direction=Direction.RIGHT

        # self.head=[self.width/2,self.height/2]
        self.head=Point(self.width/2,self.height/2)

        # rest of the body of snake
        self.snake= [self.head,Point(self.head.x-BLOCK_SIZE,self.head.y),Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]

        self.score=0

        #Food
        self.food=None
        self._place_food()
        self.reset()


    def reset(self):
        self.direction=Direction.RIGHT

        # self.head=[self.width/2,self.height/2]
        self.head=Point(self.width/2,self.height/2)

        # rest of the body of snake
        self.snake= [self.head,Point(self.head.x-BLOCK_SIZE,self.head.y),Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]

        self.score=0

        #Food
        self.food=None
        self._place_food()
        self.iteration=0
        

    def _place_food(self):
        x= random.randint(1,(self.width-BLOCK_SIZE)//BLOCK_SIZE-1)*BLOCK_SIZE
        y= random.randint(1,(self.height-BLOCK_SIZE)//BLOCK_SIZE-1)*BLOCK_SIZE
        self.food=Point(x,y)
        if self.food in self.snake:
            self._place_food()
        
    #playing

    def play_step(self,action):
        self.iteration+=1
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                print("Game Over")
                quit()
            
                                     
                
        #move snake
        self.move(action)
        self.snake.insert(0,self.head)

        reward=0
        #check if game over->ouit
        game_over=False
        if self.is_collision() or  self.iteration> 100*len(self.snake):
            game_over=True
            reward=-10
            return reward,game_over,self.score
        
        #place new food ->if food is eaten or just move snake

        if self.head == self.food:
            self.score+=1
            reward=+10
            self._place_food()
        else:
            self.snake.pop()    

        #update UI and clock
        self.update_ui()
        self.clock.tick(FPS)
        #return game over and score
        
        return reward,game_over,self.score



    def is_collision(self,pt=None):
        if pt==None:
            pt=self.head

        if pt.x>=self.width - BLOCK_SIZE or pt.x<=0 or pt.y>=self.height- BLOCK_SIZE or pt.y<=0:
            return True
        #hits itself
        if pt in self.snake[1:]:
            return True
        return False


    def update_ui(self):
        self.display.fill(BLACK)

     # Draw the purple border
        pygame.draw.rect(self.display, PURPLE, pygame.Rect(0, 0, self.width, BLOCK_SIZE))
        pygame.draw.rect(self.display, PURPLE, pygame.Rect(0, 0, BLOCK_SIZE, self.height))
        pygame.draw.rect(self.display, PURPLE, pygame.Rect(0, self.height - BLOCK_SIZE, self.width, BLOCK_SIZE))
        pygame.draw.rect(self.display, PURPLE, pygame.Rect(self.width - BLOCK_SIZE, 0, BLOCK_SIZE, self.height))

        for i, point in enumerate(self.snake):
            if i == 0:
                pygame.draw.circle(self.display, BLUE1, (point.x + BLOCK_SIZE // 2, point.y + BLOCK_SIZE // 2), BLOCK_SIZE // 2)
                pygame.draw.circle(self.display, BLUE2, (point.x + BLOCK_SIZE // 2, point.y + BLOCK_SIZE // 2), BLOCK_SIZE // 4)
            else:
                pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x + 4, point.y + 4, 12, 12))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
    

    def move(self,action):
        #[straight,right,left]
        clock_wise=[Direction.RIGHT,Direction.DOWN,Direction.LEFT,Direction.UP]
        idx=clock_wise.index(self.direction)

        if np.array_equal(action,[1,0,0]):
            new_direction=clock_wise[idx]#no change
        elif np.array_equal(action,[0,1,0]):
            new_idx=(idx+1)%4
            new_direction=clock_wise[new_idx]#right turn
        else:#[0,0,1]
            new_idx=(idx-1)%4
            new_direction=clock_wise[new_idx]#left turn

        self.direction=new_direction

        x=self.head.x
        y=self.head.y

        if self.direction==Direction.RIGHT:
            x+=BLOCK_SIZE
        elif self.direction==Direction.LEFT: 
            x-=BLOCK_SIZE
        elif self.direction==Direction.UP:
            y-=BLOCK_SIZE           
        elif self.direction==Direction.DOWN:                     
            y+=BLOCK_SIZE
       
        self.head=Point(x,y)    



# if __name__ == "__main__":
#     game = SnakeGameAI()

#     # Game loop
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:  # Restart on Enter key
#                     game = SnakeGameAI()
#                 elif event.key == pygame.K_ESCAPE:  # Quit on Escape key
#                     running = False
#                 elif event.key == pygame.K_LEFT:
#                     game.direction = Direction.LEFT
#                 elif event.key == pygame.K_RIGHT:
#                     game.direction = Direction.RIGHT
#                 elif event.key == pygame.K_UP:
#                     game.direction = Direction.UP
#                 elif event.key == pygame.K_DOWN:
#                     game.direction = Direction.DOWN
        
#         game_over, score = game.play_step()

#         if game_over:
#             print("Final Score", score)

#             pygame.time.delay(2000)  # Delay for 2000 milliseconds (2 seconds)

#             waiting_for_action = True
#             while waiting_for_action:
#                 for event in pygame.event.get():
#                     if event.type == pygame.QUIT:
#                         pygame.quit()
#                         quit()
#                     if event.type == pygame.KEYDOWN:
#                         if event.key == pygame.K_RETURN:
#                             game = SnakeGameAI()
#                             waiting_for_action = False
#                         elif event.key == pygame.K_ESCAPE:
#                             pygame.quit()
#                             quit()

#     pygame.quit()
#     quit()




