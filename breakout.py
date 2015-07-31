#s15008
from tkinter import *
import random
import time

def point_collision(a, b):
    cx = (b[2] - b[0]) /2
    cy = (b[3] - b[0]) /2
    r = cx
    #left-top
    dx = cx - a[0]
    dy = cx - a[1]
    p1 = dx**2 + dy**2 < r**2
    #right-top
    dx = cx - a[2]
    dy = cy - a[1]
    p2 = dx**2 + dy**2 < r**2
    #right-bottom
    dx = cx - a[2]
    dy = cy - a[3]
    p3 = dx**2 + dy**2 < r**2
    #left-bottom
    dx = cx - a[0]
    dy = cy - a[3]
    p4 = dx**2 + dy**2 < r**2

    return p1 or p2 or p3 or p4


class Ball:
    def __init__(self, canvas, paddle, blocks, speed, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.speed = speed
        self.blocks = blocks
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 300)
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = 0
        self.y = 0
        self.canvas.bind_all("<Button-1>",self.game_start)
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.hit_bottom = False

    def game_start(self, evt):
        self.x = -self.speed
        self.y = self.speed
        
    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
            return False

    def hit_block(self, pos):
        
        collision_type = 0
        for block in self.blocks:
            block_pos = self.canvas.coords(block.id)
            #circle_collision check
            if point_collision(block_pos, pos):
                collision_type |=3
            #top check
            if pos[2] >= block_pos[0] and pos[0] <= block_pos[2] \
               and pos[3] >= block_pos[1] and pos[3] < pos[3]:
                collision_type |= 1
            #bottom check
            if pos[2] >= block_pos[0] and pos[0] <= block_pos[2] \
               and pos[1] > block_pos[1] and pos[1] <=block_pos[3]:
                collision_type |= 1
            #left check
            if pos[3] >= block_pos[1] and pos[1] <= block_pos[3] \
               and pos[2] >= block_pos[0] and pos[2] < block_pos[2]:
                collision_type |=2
            #right check
            if pos[3] >= block_pos[1]and pos[1] <= block_pos[3] \
               and pos[0] > block_pos[0] and pos[0] <= block_pos[2]:
                collision_type |= 2
                self.score.hit()

            if collision_type !=0:
                return (block, collision_type)

        return(None, 0)

                
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y *= -1
        if pos [3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = self.y * -1
            if self.y > -13:
                self.y += -0.5
                print(self.y)
        if pos[0] <= 0:
            self.x *= -1
        if pos[2] >= self.canvas_width:
            self.x *= -1
        (target, collision_type) = self.hit_block(pos)
        if target != None:
            target.delete()
            del self.blocks[self.blocks.index(target)]
            if (collision_type & 1) != 0:
                self.y *= -1
                self.x *= -1
            if (collision_type & 2) != 0:
                self.x *= -1
        

class Paddle:
    def __init__(self, canvas, speed, color):
        self.canvas = canvas
        self.speed = speed
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 600)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all("<KeyPress-Left>", self.turn_left)
        self.canvas.bind_all("<KeyPress-Right>", self.turn_right)

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt):
        self.x = -self.speed

    def turn_right(self, evt):
        self.x = self.speed
        

class Block:
    def __init__(self, canvas, x, y, color):
        self.canvas = canvas
        self.pos_x = x
        self.pos_y = y
        self.id = canvas.create_rectangle(0, 0, 50, 20, fill=color)
        self.canvas.move(self.id, 25 + self.pos_x * 50, 25 + self.pos_y * 20)

    def delete(self):
        self.canvas.delete(self.id)
        

class Score:
    def __init__(self, canvas, fontsize, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(250, 400, text="score: %s" % self.score, font=("Times",35), fill=color)

    def hit(self):
        self.score += 100
        self.canvas.itemconfig(self.id, text="score: %s" % self.score)
        
class Gameclear:
    def __init__(self, canvas, x, y, text, fontsize, color):
        self.canvas = canvas
        self.id = canvas.create_text(x, y, text=text, font=("Times", fontsize), fill=color, state="hidden")

    def show(self):
        self.canvas.itemconfig(self.id, state="normal")

class Gameover:
    def __init__(self, canvas, x, y, text, fontsize, color):
        self.canvas = canvas
        self.id = canvas.create_text(x, y, text=text, font=("Times", fontsize), fill=color, state="hidden")

    def show(self):
        self.canvas.itemconfig(self.id, state="normal")



#config
WIDTH = 500
HEIGHT = 700
FPS = 50
BALL_SPEED = 3
PADDLE_SPEED = 3
COLORS = {0:"green", 1:"black"}
BLOCK_Y = 6
BLOCK_X = 9
BLOCK_LIST =[0,0,0,0,0,0,0,0,0,
             0,1,1,0,0,0,1,1,0,
             0,1,1,0,0,0,1,1,0,
             0,0,0,0,1,0,0,0,0,
             0,0,1,1,1,1,1,0,0,
             0,0,1,1,0,1,1,0,0
             ]



#initialize
tk = Tk()
tk.title("Breakout")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

blocks = []
for y in range(BLOCK_Y):
    for x in range(BLOCK_X):
        blocks.append(Block(canvas, x, y, COLORS[BLOCK_LIST[x + y * 9]]))

score = Score(canvas, 20, 'green')
paddle = Paddle(canvas, PADDLE_SPEED, "blue")
ball = Ball(canvas, paddle, blocks, BALL_SPEED, "red")
gameclear = Gameclear(canvas, 250, 200, "よくできました＾＾;", 40, "red")
gameover = Gameover(canvas, 250, 200, "まあまあですね＾＾", 40, "red")

while True:
    if score.score == 4100:
        gameclear.show()
    elif ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    else:
        gameover.show()
        break


    tk.update_idletasks()
    tk.update()
    time.sleep(1/FPS)
