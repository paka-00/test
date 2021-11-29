import pyxel
import numpy as np
import random

WINDOW_X = 200
WINDOW_Y = 200
PLAYER_X = 16
PLAYER_Y = 16
BOARD_X = 20


class vec:
    def __init__(self,x,y):
        self.x=x
        self.y=y

class player:
    def __init__(self,id):
        self.pos = vec(WINDOW_X/2,WINDOW_Y-PLAYER_Y)
        self.img = id
        self.vec_x = 0
        self.vec_y = 0

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
        self.img=id
        self.vec_x=0

    def update(self,x,y,dx):
        self.pos.x=x
        self.pos.y=y
        self.vec_x=dx

class App:
    def __init__(self):
        self.id_0=0
        pyxel.init(WINDOW_X,WINDOW_Y,caption='JUMP')
        pyxel.load("assets/space.pyxres")
        self.player=player(self.id_0)
        self.gravity=1
        self.ground=1
        self.direction=-1
        self.jump=0
        self.board=[]
        pyxel.run(self.update,self.draw)

    def update(self):
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()
        self.update_player()
        self.update_board()
    
    def update_player(self):
        if self.player.pos.y+PLAYER_Y==WINDOW_Y:
            self.ground=1
            self.player.vec_y=0
        else:
            self.ground=0
        
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direction=-1
            self.player.vec_x-=1
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.direction=1
            self.player.vec_x+=1
        else :self.player.vec_x-=np.sign(self.player.vec_x)

        if pyxel.btn(pyxel.KEY_SPACE) and self.ground==1:
            self.player.vec_y-=5
            self.jump=5

        if pyxel.btn(pyxel.KEY_SPACE) and self.jump>0:
            self.jump-=1
            self.player.vec_y-=2

        if self.ground==0:
            self.player.vec_y+=self.gravity
        self.player.pos.y+=self.player.vec_y
        if self.player.pos.y+PLAYER_Y>=WINDOW_Y:
            self.player.pos.y=WINDOW_Y-PLAYER_Y
        
        self.player.pos.x+=self.player.vec_x
        if np.abs(self.player.vec_x)>100:
            self.player.vec_x=np.sign(self.player.vec_x)*100
        
    def update_board(self):
        r=random.randint(0,WINDOW_Y-PLAYER_Y)
        if r%100==0:
            self.board.append(board(self.id_0))
            self.board[-1].pos.y=random.randint(3*PLAYER_Y,self.player.pos.y)
            if random.randint(0,2)==0:
                self.board[-1].pos.x = 0-BOARD_X
                self.board[-1].vec = 1
            else:
                self.board[-1].pos.x=WINDOW_X
                self.board[-1].vec=-1

        for i in self.board:
            i.pos.x+=i.vec
            if i.vec==1 and i.pos.x>WINDOW_X:
                self.board.pop(self.board.index(i))
            elif i.vec==-1 and i.pos.x+BOARD_X<0:
                self.board.pop(self.board.index(i))
                

    def draw(self):
        pyxel.cls(0)
        if self.direction==-1:
            pyxel.blt(self.player.pos.x%WINDOW_X, self.player.pos.y, self.id_0,0,0,16,16,13)
        else:
            pyxel.blt(self.player.pos.x%WINDOW_X, self.player.pos.y, self.id_0,0,0,-16,16,13)
        for i in self.board:
            pyxel.rect(i.pos.x, i.pos.y, BOARD_X, 2, 3)
App()