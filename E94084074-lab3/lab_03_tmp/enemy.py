import pygame
import math
import os
from settings import PATH


pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))
#設定全域變數(pathcounter)使能進行路徑變化
pathcounter=-1




class Enemy:
    
    def __init__(self):
        #初始化所有數值
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        #將全域變數變成self.pathcounter，方便使用在move函數
        self.pathcounter=pathcounter            
        self.path_pos = 0
        self.move_count = 0
        self.stride = 1
        #判斷敵人該走哪條路徑(運用餘數輪流走~)
        if ((self.pathcounter%2)==0):
            self.path=PATH[0]
        elif((self.pathcounter%2)!=0):
            self.path=PATH[1]
        self.x, self.y = self.path[0]
    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        # 利用上面敵人的位置去進行設置，綠色血條跟hp成比例，接續綠色血條，列印出剩下的紅色血條(位置一樣是在敵人上方~)
        pygame.draw.rect(win, (0,255,0), [self.x - self.width // 2,self.y - self.height // 2-7, self.width*(self.health/self.max_health), 7])
        pygame.draw.rect(win, (255,0,0), [self.x - self.width // 2+self.width*(self.health/self.max_health),self.y - self.height // 2-7,self.width*((self.max_health-self.health)/self.max_health) , 7])
        return None
       
        

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        
        # x, y position of point A
        #判斷敵人該走哪條路徑(運用餘數輪流走~)
        if ((self.pathcounter%2)==0):
            self.path=PATH[0]
        elif((self.pathcounter%2)!=0):
            self.path=PATH[1]
            
        #利用助教給的example~    
        x0,y0=self.path[self.path_pos]
        x1,y1 =self.path[self.path_pos+1]
        distance_A_B = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
        max_count = int(distance_A_B / self.stride)  # total footsteps that needed from A to B
        #判斷是否走到了該位置點上
        if self.move_count < max_count:
            unit_vector_x = (x1 - x0) / distance_A_B
            unit_vector_y = (y1 - y0) / distance_A_B
            delta_x = unit_vector_x * self.stride
            delta_y = unit_vector_y * self.stride

            # update the coordinate and the counter
            self.x += delta_x
            self.y += delta_y
            self.move_count += 1
           
            
        
        #判斷是否走到了該位置點上 (和判斷是否為終點)，不然將點1和點2，換成點2和點3(並重置self.move_count)!
        if(self.path_pos<=len(self.path)-1 and self.move_count >= max_count):
            self.move_count=0
            self.path_pos += 1
            self.x,self.y=self.path[self.path_pos]
        
         
        return None
    
        
        
   

class EnemyGroup:
    
    def __init__(self):
        self.gen_count = 0
        self.gen_period = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = []  # don't change this line until you do the EX.3 
        
    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """

        # Hint: self.expedition.append(self.reserved_members.pop())
        # self.gen_count(幀數判斷，當self.gen_count=self.gen_period時且self.reserved_members不是空的，此時輸出敵人，達到間隔的作用)
        
        self.gen_count+=1
        
        if(self.gen_count >=self.gen_period and self.reserved_members!=[] ):
            
            self.gen_count=0    #重置幀數
            self.expedition.append(self.reserved_members.pop())
            

        return None

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        #設定全域變數(pathcounter)使能進行路徑變化，每次按下按鍵pathcounter+=1
        #利用for迴圈 for i in range(num) ,num=3,重複輸入3個敵人去self.reserved_members
        global  pathcounter
        pathcounter+=1
        for i in range(num):
            self.reserved_members.append(Enemy())
        
        
                
            
        return None

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)
    
        




