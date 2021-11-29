import pyxel
import numpy as np
import random
import os

WINDOW_X = 200
WINDOW_Y = 200
PLAYER_X = 16
PLAYER_Y = 16
ENEMY_1_X = 16
ENEMY_1_Y = 12 
BOARD_X = 20
ENEMY_2_X = 16
ENEMY_2_Y = 16
HIGHT = 2000
heart = 2000


class vec:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class player:
    def __init__(self,id):
        self.pos = vec(WINDOW_X/2,WINDOW_Y/2-PLAYER_Y)
        self.img = id
        self.vec_x = 0
        self.vec_y = 0
        self.hp = 3

    def update(self,x,y,dx,dy):
        self.pos.x = x
        self.pos.y = y
        self.vec_x = dx
        self.vec_y = dy

class board:
    def __init__(self,id):
        self.pos=vec(255,255)
        self.vec=0
        self.img=id
    
    def update(self,x,y,dx):
        self.pos.x=x
        self.pos.y=y
        self.vec=dx
        
class enemy:
    def __init__(self,id):
        self.pos=vec(255,255)
        self.size=vec(0,0)
        self.id=id
        self.vec_x=0
        self.vec_y=0
        self.atack=[]
        self.hp=0

    def update(self,x,y,dx,dy):
        self.pos.x=x
        self.pos.y=y
        self.vec_x=dx
        self.vec_y=dy
        self.update_atack()
    
    def update_atack(self):
        r=random.ramdint(0,1)


class main:
    def __init__(self):
        self.id_0=0
        pyxel.init(WINDOW_X,WINDOW_Y,caption='JUMP')
        pyxel.load("assets/space.pyxres")
        self.init()
        if os.path.exists('score_max.txt'):
            f=open('score_max.txt','r')
            self.score_max = int(f.read())
            f.close
        else :self.score_max = 0
        pyxel.run(self.update,self.draw)

    def init(self):
        self.player=player(self.id_0)
        self.gravity=2
        self.jump = 5
        self.space = 0
        self.time = 0
        self.hight = HIGHT
        self.score=0
        self.invin = 5
        self.life=1
        self.energy = 10
        self.direction=-1
        self.enemy_1=[]
        self.enemy_2=[]
        self.enemy_3=[]
        self.enemy_4=[]
        self.h = self.h=board(0)
        self.atack=[]
        self.drop=[]
        self.para=[]
        self.minus=0

    def update(self):
        self.score_max=max(self.score+self.hight//10,self.score_max)
        if pyxel.btn(pyxel.KEY_Q):
            f = open('score_max.txt', 'w')
            f.write(str(self.score_max))
            f.close

            pyxel.quit()
        if self.player.hp>=0:
            self.update_player()
            self.update_enemy()
            self.update_atack()
            self.time+=1
            if self.minus==1 and self.hight>0:
                self.hight-=1
            elif self.minus==1 and self.hight<=0:
                self.hight=0
            else:
                self.hight+=1
        else:
            if self.life==1:
                self.score+=self.hight//10
                self.life=0
            if pyxel.btn(pyxel.KEY_R):
                self.init()
        r=random.randint(0,heart)
        if r==0 and self.h.pos.x==255:
            self.heart()

        if self.h.pos.x<255 and self.player.hp>=0:
            self.update_heart()
            

    def heart(self):
        self.h.pos.x=random.randint(0,WINDOW_X)
        self.h.pos.y=0
        self.h.vec=1
    
    def update_heart(self):
        self.h.pos.y+=1
        if self.h.pos.x<self.player.pos.x+PLAYER_X and self.h.pos.x+8>self.player.pos.x and self.h.pos.y<self.player.pos.y+PLAYER_Y and self.h.pos.y+8>self.player.pos.y:
            self.player.hp += 1
            self.h.pos.x=255

        if self.h.pos.y>255:
            self.h.pos.x=255
        




    def bomb(self):
        s1,s2 = len(self.enemy_1),len(self.enemy_2)
        s3,s4 = len(self.enemy_3),len(self.enemy_4)
        self.score += (s1+s2+s3+s4)*100
        self.drop=[]
        self.para=[]
        self.enemy_1=[]
        self.enemy_2=[]
        self.enemy_3=[]
        self.enemy_4=[]
        self.energy -= 10 

    def update_player(self):
        if self.invin>0:
            self.invin-=1
        if pyxel.btn(pyxel.KEY_LEFT) and self.player.pos.x>0:
            self.direction=-1
            self.player.vec_x-=1
        elif pyxel.btn(pyxel.KEY_RIGHT) and self.player.pos.x<WINDOW_X-PLAYER_X:
            self.direction=1
            self.player.vec_x+=1
        else :self.player.vec_x-=np.sign(self.player.vec_x)#x座標
            
        if pyxel.btn(pyxel.KEY_UP):
            self.player.vec_y=-self.jump
            self.space=1
        else:self.space=0#ジャンプ制御

        if pyxel.btnp(pyxel.KEY_B) and self.energy>=10:
            self.bomb()

        if self.player.vec_y<0:
            self.player.vec_y+=self.gravity

        else:self.player.vec_y=self.gravity#落下制御

        self.player.pos.y+=self.player.vec_y

        if self.player.pos.y+PLAYER_Y>=WINDOW_Y:
            self.player.pos.y=WINDOW_Y-PLAYER_Y
        elif self.player.pos.y<0:
            self.player.pos.y=0
            
        self.player.pos.x+=self.player.vec_x

        if self.player.pos.x<=0:self.player.pos.x=0
        elif self.player.pos.x>=WINDOW_X-PLAYER_X:
            self.player.pos.x=WINDOW_X-PLAYER_X

        if np.abs(self.player.vec_x)>5:
            self.player.vec_x=np.sign(self.player.vec_x)*5

        if self.player.pos.y+PLAYER_Y==WINDOW_Y:
            self.minus=1
        else:
            self.minus=0
        
        if pyxel.btnp(pyxel.KEY_V) and self.energy>0:
            self.atack.append(board(self.id_0))
            self.atack[-1].pos.x = self.player.pos.x+PLAYER_X*1*(self.direction>0)
            self.atack[-1].pos.y = self.player.pos.y+PLAYER_Y/2
            self.atack[-1].vec = self.direction*(np.abs(self.player.vec_x)//3+1)
            self.energy-=1
        
        if self.time%200==1:
            self.energy+=1

    def update_enemy(self):
        if self.hight<1000:
            r=random.randint(0,50)
            if r==0:
                self.enemy_1.append(enemy(1))
                r=random.choice((-1,1))
                if r<0:
                    self.enemy_1[-1].pos.x = WINDOW_X-ENEMY_1_X
                else:self.enemy_1[-1].pos.x = 0
                self.enemy_1[-1].pos.y = random.randint(0,WINDOW_Y-ENEMY_1_Y)
                self.enemy_1[-1].vec_x = r
                self.enemy_1[-1].size.x=ENEMY_1_X
                self.enemy_1[-1].size.y=ENEMY_1_Y

        elif self.hight>1000 and self.hight<=3500:
            r=random.randint(0,75)
            if r==0:
                self.enemy_2.append(enemy(2))
                r=random.choice((-1,1))
                if r<0:
                    self.enemy_2[-1].pos.x = WINDOW_X-ENEMY_1_X
                else:self.enemy_2[-1].pos.x = 0
                self.enemy_2[-1].pos.y = random.randint(0,WINDOW_Y-ENEMY_1_Y)
                self.enemy_2[-1].vec_x = r
                self.enemy_2[-1].size.x=ENEMY_2_X
                self.enemy_2[-1].size.y=ENEMY_2_Y
                self.enemy_2[-1].hp=random.randint(0,WINDOW_X-ENEMY_2_X)

        r=random.randint(0,75)
        if ((self.hight>2000  and self.hight<=3500) or self.score>5000) and r==1:

            self.para.append(enemy(3))
            self.para[-1].pos.x=random.randint(0,WINDOW_X)-16
            self.para[-1].pos.y=0
            self.para[-1].vec_y=1
            self.para[-1].vec_x=random.choice((-1,1))
            self.para[-1].size.x=8
            self.para[-1].size.y=8
            self.para[-1].hp=400
        
        if (self.hight>3500 or self.score>8500) and r==2:
            self.enemy_3.append(enemy(4))
            x=random.choice((0,WINDOW_X))
            y=random.randint(0,WINDOW_Y-ENEMY_1_Y)
            self.enemy_3[-1].pos.y = y
            self.enemy_3[-1].pos.x = x-16
            self.enemy_3[-1].size.x=16
            self.enemy_3[-1].size.y=16
            self.enemy_3[-1].vec_x=np.sign(self.player.pos.x-x)
            self.enemy_3[-1].vec_y=np.sign(self.player.pos.y-y)
            self.enemy_3[-1].hp=400
        
        if (self.hight>4000 or self.score>10000)and r==0:
            self.enemy_4.append(enemy(4))
            x=random.choice((0,WINDOW_X))
            y=random.randint(0,WINDOW_Y-ENEMY_1_Y)
            self.enemy_4[-1].pos.y = y
            self.enemy_4[-1].pos.x = x-16
            self.enemy_4[-1].size.x=16
            self.enemy_4[-1].size.y=16
            self.enemy_4[-1].vec_x=np.sign(self.player.pos.x-x)
            self.enemy_4[-1].vec_y=np.sign(self.player.pos.y-y)
            self.enemy_4[-1].hp= 2

        if len(self.enemy_4)!=0:
            self.update_4(self.enemy_4,1)
            

        if len(self.enemy_1)!=0:
            self.update_enemy_list(self.enemy_1,1,1)
        if len(self.enemy_2)!=0:
            self.update_enemy_list(self.enemy_2,2,2)
        if len(self.drop)!=0:
            self.update_drop(self.drop,1)
            self.update_enemy_list(self.drop,2,0)
        if len(self.para)!=0:
            self.update_drop(self.para,2)
            self.update_enemy_list(self.para,2,0)  
        if len(self.enemy_3)!=0:
            self.update_enemy_list(self.enemy_3,3,1)  

    def update_4(self,ene_list,v):
            for i in ene_list:
                for j in self.atack: 
                    if j.pos.x>i.pos.x and j.pos.x<i.pos.x+i.size.x and j.pos.y>i.pos.y and j.pos.y<i.pos.y+i.size.y:
                        ene_list.pop(ene_list.index(i))
                        self.atack.pop(self.atack.index(j))
                        self.energy+=i.id
                        self.score+=100*i.id

                if i in ene_list:
                    i.vec_x = np.sign(self.player.pos.x-i.pos.x)
                    i.vec_y = np.sign(self.player.pos.y-i.pos.y)
                    i.pos.x += i.vec_x*v
                    i.pos.y += i.vec_y*v
                    if i.pos.x>WINDOW_X or i.pos.x<0 :
                        ene_list.pop(ene_list.index(i))
                    if  self.invin==0 and i.pos.x<self.player.pos.x+PLAYER_X and i.pos.x+i.size.x>self.player.pos.x and i.pos.y<self.player.pos.y+PLAYER_Y and i.pos.y+i.size.y>self.player.pos.y:
                        
                        self.player.hp-=1
                        self.invin = 80
                        ene_list.pop(ene_list.index(i)) 

    def update_enemy_list(self,ene_list,v,id):
        for i in ene_list:
            for j in self.atack: 
                if j.pos.x>i.pos.x and j.pos.x<i.pos.x+i.size.x and j.pos.y>i.pos.y and j.pos.y<i.pos.y+i.size.y:
                    ene_list.pop(ene_list.index(i))
                    self.atack.pop(self.atack.index(j))
                    self.energy+=2*i.id
                    self.score+=100*i.id

            if i in ene_list:
                i.pos.x += i.vec_x*v
                i.pos.y += i.vec_y
                if i.pos.x>WINDOW_X or i.pos.x<0 :
                    ene_list.pop(ene_list.index(i))
                if  self.invin==0 and i.pos.x<self.player.pos.x+PLAYER_X and i.pos.x+i.size.x>self.player.pos.x and i.pos.y<self.player.pos.y+PLAYER_Y and i.pos.y+i.size.y>self.player.pos.y:
                    
                    self.player.hp-=1
                    self.invin = 80
                    ene_list.pop(ene_list.index(i))
                
                if id==2 and i.hp==i.pos.x:
                    self.drop.append(enemy(0))
                    self.drop[-1].pos.x=i.pos.x
                    self.drop[-1].pos.y=i.pos.y+ENEMY_2_Y
                    self.drop[-1].vec_y=2
                    self.drop[-1].size.x=8
                    self.drop[-1].size.y=8
                    self.drop[-1].hp=200

    def update_drop(self,d,id):
        for i in d:
            if id==2 and self.hight%10==0:
                i.vec_x=np.sign(self.player.pos.x-i.pos.x)
            i.pos.y+=i.vec_y
            i.pos.x+=i.vec_x
            if i.pos.x<0 or i.pos.x>WINDOW_X or i.pos.y<0 or i.pos.y>WINDOW_Y:
                d.pop(d.index(i))
            for j in self.atack: 
                if j.pos.x>i.pos.x and j.pos.x<i.pos.x+i.size.x and j.pos.y>i.pos.y and j.pos.y<i.pos.y+i.size.y:
                    d.pop(d.index(i))
                    self.score+=i.hp
                    self.atack.pop(self.atack.index(j))

    
            
    def draw_enemy(self):
        if len(self.enemy_1)!=0:
            d = self.hight%4
            if d>1:d=1
            else:d=0
            for i in self.enemy_1:
                if i.vec_x>0:
                    pyxel.blt(i.pos.x, i.pos.y, self.id_0,32+d*ENEMY_1_X,0,ENEMY_1_X,ENEMY_1_Y,13)
                else:pyxel.blt(i.pos.x, i.pos.y, self.id_0,32+d*ENEMY_1_X,0,-ENEMY_1_X,ENEMY_1_Y,13)
            for i in self.enemy_1:
                if i.vec_x>0:
                    pyxel.blt(i.pos.x, i.pos.y, self.id_0,32+d*ENEMY_1_X,0,ENEMY_1_X,ENEMY_1_Y,13)
                else:pyxel.blt(i.pos.x, i.pos.y, self.id_0,32+d*ENEMY_1_X,0,-ENEMY_1_X,ENEMY_1_Y,13)
        
        if len(self.enemy_2)!=0:
            for i in self.enemy_2:
                pyxel.blt(i.pos.x, i.pos.y, self.id_0,32,16,ENEMY_2_X*-1*i.vec_x,ENEMY_2_Y,14)
        if len(self.drop)!=0:
            for i in self.drop:
                pyxel.blt(i.pos.x, i.pos.y, self.id_0,48,16,8,8,14)

        if len(self.para)!=0:
            for i in self.para:
                pyxel.blt(i.pos.x, i.pos.y, self.id_0,56,16,8,8,14)

        if len(self.enemy_3)!=0:
            for i in self.enemy_3:
                pyxel.blt(i.pos.x, i.pos.y, self.id_0,16,32,16*-1*i.vec_x,16,13)

        if len(self.enemy_4)!=0:
            for i in self.enemy_4:
                pyxel.blt(i.pos.x, i.pos.y, self.id_0,0,32,16,16,13)
        if self.h!=0:
            pyxel.blt(self.h.pos.x,self.h.pos.y,0,48,24,8,8,14)

    def update_atack(self):
        for i in self.atack:
            i.pos.x+=i.vec*2
            if i.pos.x>WINDOW_X or i.pos.x<0:
                self.atack.pop(self.atack.index(i))

    def draw(self):
        pyxel.cls(0)
        if self.player.hp<0:
            pyxel.cls(0)
            pyxel.text(10,40,"QUIT PRESS Q",13)
            pyxel.text(10,50,"RESTART PRESS R",13)
        
        elif self.hight>0 and self.hight<4000:
            for i in range(0,WINDOW_X//16+1):
                for j in range(0,WINDOW_Y//16+1):
                    pyxel.blt(32*i,16*j+self.hight%WINDOW_Y,0,0,16,32,16)
                    pyxel.blt(32*i,16*j+self.hight%WINDOW_Y-WINDOW_Y,0,0,16,32,16)

        elif self.hight>4000:
            for i in range(0,WINDOW_X//16+1):
                for j in range(0,WINDOW_Y//16+1):
                    pyxel.blt(48*i,16*j+self.hight%WINDOW_Y,0,0,48,16,48)
                    pyxel.blt(48*i,16*j+self.hight%WINDOW_Y-WINDOW_Y,0,0,48,16,48)
                    
        else:
            self.score-=1
            for i in range(0,WINDOW_X//16+1):
                for j in range(0,WINDOW_Y//16+1):
                    pyxel.blt(32*i,16*j,0,0,16,32,16)
                    pyxel.blt(32*i,16*j,0,0,16,32,16)
        
                
        
       
        pyxel.blt(self.player.pos.x, self.player.pos.y, self.id_0,16-16*self.space,0,-16*self.direction,16,(13+self.invin)%16)
        
    
        
        for i in self.atack:
            pyxel.circ(i.pos.x,i.pos.y,1,9)
        pyxel.text(10,10,"SCORE "+str(self.score+self.hight//10)+"  ENERGY  "+str(self.energy),13)
        pyxel.text(10,20,"HP"+str(self.player.hp),13)
        pyxel.text(50,20,"MAX "+str(self.score_max),13)
        self.draw_enemy()
        
        
        
main()