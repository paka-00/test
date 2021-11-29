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

class App:
    def __init__(self):
        self.id_0=0
        self.id_1=1
        self.id_1_x=window_x/2-38
        self.id_1_y=window_y/2-16
        self.velocity=5
        pyxel.init(window_x,window_y,caption='Hello Pyxel')
        pyxel.load("C:/Users/東　大介/.vscode/test/pyxel-master/pyxel/pyxel_examples/assets/test.pyxres")
        pyxel.image(self.id_1).load(0,0,"assets/pyxel_logo_38x16.png")
        self.cat=chara(self.id_1)
        self.clk=1
        self.fire=chara(self.id_1)
        self.fire.pos.x,self.fire.pos.y=255,255
        self.f=0
        self.dx_fire=0

        self.slime=chara(self.id_1)
        self.slime_pop=[1]
        self.slime.pos.x,self.slime.pos.y=40,40
        pyxel.run(self.update,self.draw)
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_0):
            pyxel.quit()
        dx = pyxel.mouse_x - self.cat.pos.x  # x軸方向の移動量(マウス座標 - cat座標)
        dy = pyxel.mouse_y - self.cat.pos.y  # y軸方向の移動量(マウス座標 - cat座標)
        
        if dx != 0:
            self.cat.update(pyxel.mouse_x, pyxel.mouse_y, dx) # 座標と向きを更新
            
        elif dy != 0:
            self.cat.update(pyxel.mouse_x, pyxel.mouse_y, self.cat.vec) # 
        self.fire.update(self.fire.pos.x+self.velocity*self.dx_fire,self.fire.pos.y,dx)
        if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
            self.clk*=-1
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
            self.f=1
            self.fire.pos.x,self.fire.pos.y=self.cat.pos.x,self.cat.pos.y
            self.dx_fire=np.sign(self.cat.vec)
        if self.fire.pos.x<self.slime.pos.x+16 and self.fire.pos.x>self.slime.pos.x-16 and len(self.slime_pop)>0 and self.fire.pos.y<self.slime.pos.y+16 and self.fire.pos.y>self.slime.pos.y-16:
            self.slime_pop.pop()
            
        
        if self.fire.pos.x<0 or self.fire.pos.y<0:
            self.fire.pos.x,self.fire.pos.y=255,255
        
        
       
 
    def draw(self):
        pyxel.cls(0)
        #pyxel.blt(self.id_1_x, self.id_1_y, self.id_1, 0, 0, 38, 16)
        if self.clk==1:
            cha=16
        else: cha=0
        if self.cat.vec > 0:
            pyxel.blt(self.cat.pos.x, self.cat.pos.y, self.id_0,cha,0,16,16,13)
        else:
            pyxel.blt(self.cat.pos.x, self.cat.pos.y, self.id_0,cha,0,-16,16,13)
        if self.f==1:
            pyxel.blt(self.fire.pos.x,self.fire.pos.y,self.id_0,0,17,16,16,13)
        if len(self.slime_pop) != 0: 
            pyxel.blt(40,40,self.id_0,17,17,16,16,13)
        if len(self.slime_pop)==0:
            pyxel.text(50, 50, "CLEAR", 2)
App()