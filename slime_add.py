import pyxel
import numpy as np
import random

window_x=160
window_y=160

class vec:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class chara:
    def __init__(self,id):
        self.pos=vec(255,255)
        self.img_cat=id
        self.vec=0


    def update(self,x,y,dx):
        self.pos.x=x
        self.pos.y=y
        self.vec=dx

class enemy:
    def __init__(self,id):
        self.pos=vec(255,255)
        self.img_enemy=id
        self.vec=0
    
    def update(self,x,y,dx):
        self.pos.x = x
        self.pos.y = y
        self.vec = dx

class App:
    def __init__(self):
        self.id_0=0
        self.id_1=1
        self.id_1_x=window_x/2-38
        self.id_1_y=window_y/2-16
        self.velocity=5
        pyxel.init(window_x,window_y,caption='Hello Pyxel')
        pyxel.load("assets/test.pyxres")
        pyxel.image(self.id_1).load(0,0,"assets/pyxel_logo_38x16.png")
        self.cat=chara(self.id_1)
        self.clk=1
        self.fire=[]
        self.f=0
        self.slime=[]
        self.score=0
        self.game=0
        self.max_score=0
        self.babaguchi=chara(self.id_0)
        pyxel.play(0,0,loop=True) 
        pyxel.run(self.update,self.draw)
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_0):
                pyxel.quit()
        if self.game==0:
    
            dx = pyxel.mouse_x - self.cat.pos.x  
            dy = pyxel.mouse_y - self.cat.pos.y  
            
            if dx != 0:
                self.cat.update(pyxel.mouse_x, pyxel.mouse_y, dx) 
            

            elif dy != 0:
                self.cat.update(pyxel.mouse_x, pyxel.mouse_y, self.cat.vec)
            
            r=random.randint(0,30)
            if r==1:
                self.slime.append(enemy(self.id_0))
                r_x=random.randint(0,window_x)
                r_y=random.randint(0,window_y)
                while r_x>self.cat.pos.x-22 and r_x<self.cat.pos.x+22 and self.cat.pos.y<r_y+22 and self.cat.pos.y+22>r_y:
                    r_x=random.randint(0,window_x)
                    r_y=random.randint(0,window_y)

                self.slime[-1].pos.x,self.slime[-1].pos.y=r_x,r_y
            
            for j in self.slime:
                    dx_slime=np.sign(self.cat.pos.x-j.pos.x)
                    dy_slime=np.sign(self.cat.pos.y-j.pos.y)
                    j.update(j.pos.x+dx_slime,j.pos.y+dy_slime,self.cat.vec)
                    if self.cat.pos.x-14<j.pos.x and self.cat.pos.x+14>j.pos.x and self.cat.pos.y<j.pos.y+14 and self.cat.pos.y+14>j.pos.y:
                        pyxel.play(2,3)
                        self.score=0
                        self.game=1
                        self.slime=[]
                        self.fire=[]
            if self.max_score<self.score:
                self.max_score=self.score
            for i in self.fire:
                i.update(i.pos.x+self.velocity*i.vec,i.pos.y,i.vec)
                if i.pos.x>window_x or i.pos.x<0 or i.pos.y>window_y or i.pos.y<0:
                    self.fire.pop(self.fire.index(i))
                for j in self.slime:
                    if i.pos.x<j.pos.x+16 and i.pos.x>j.pos.x-16 and len(self.slime)>0 and i.pos.y<j.pos.y+16 and i.pos.y>j.pos.y-16:
                        self.slime.pop(self.slime.index(j))
                        pyxel.play(2,1)
                        self.score+=100

            if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
                self.clk*=-1
                pyxel.play(1,4)
            if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
                pyxel.play(1,2)
                self.f=1
                self.fire.append(chara(self.id_0))
                self.fire[-1].pos.x,self.fire[-1].pos.y=self.cat.pos.x,self.cat.pos.y
                self.fire[-1].vec=np.sign(self.cat.vec)
        if pyxel.btnp(pyxel.KEY_P):
            self.game=0
            
        

       
 
    def draw(self):
        pyxel.cls(0)
        pyxel.text(10,10,str(self.score),13)
        pyxel.text(30,10,"MAX "+str(self.max_score),13)
        if self.clk==1:
            cha=16
        else: cha=0
        if self.cat.vec > 0:
            pyxel.blt(self.cat.pos.x, self.cat.pos.y, self.id_0,cha,0,16,16,13)
        else:
            pyxel.blt(self.cat.pos.x, self.cat.pos.y, self.id_0,cha,0,-16,16,13)
        if self.f==1:
            for i in self.fire:
                pyxel.blt(i.pos.x,i.pos.y,self.id_0,0,16,16,16,13)
        for i in self.slime:
            pyxel.blt(i.pos.x,i.pos.y,self.id_0,16,16,16,16,13)
        if self.game==1:
            pyxel.text(60,60,"GAME OVER Press p",13)
        pyxel.blt(0,0,self.id_0,32,0,32,32,5)
App()
