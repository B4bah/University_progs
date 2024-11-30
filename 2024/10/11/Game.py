import random
from tkinter import *

window = Tk()
width = 702
height = 600
window.geometry(str(width) + 'x' + str(height))
canvas = Canvas(window, width=width, height=height, bg='lavender')
canvas.pack()
# bg_photo = PhotoImage(file='background.png')
bg_photo = PhotoImage(file='background.png')

class Knight:

    def __init__(self):
        self.vx = 0
        self.vy = 0
        self.x = 123
        self.y = height // 2
        self.photo = PhotoImage(file='knight.png')

    def up(self, event):
        if self.y <= 75: self.vy = 0; self.y += self.vy
        else: self.vy = -4; self.y += self.vy

    def down(self, event):
        if self.y >= 525: self.vy = 0; self.y += self.vy
        else: self.vy = 4; self.y += self.vy

    def right(self, event):
        if self.x >= 651: self.vx = 0; self.x += self.vx
        else: self.vx = 4; self.x += self.vx

    def left(self, event):
        if self.x <= 100: self.vx = 0; self.x += self.vx
        else: self.vx = -4; self.x += self.vx

    def stop(self, event):
        self.vx = 0
        self.vy = 0


class Dragon:

    def __init__(self):
        self.v = random.randint(1, 4)
        self.x = 650
        self.y = random.randint(100, 500)
        self.photo = PhotoImage(file='dragon.png')


knight = Knight()
dragons = []

for i in range(5):
    dragons.append(Dragon())


def game():
    canvas.delete('all')
    canvas.create_image(350, 300, image=bg_photo)
    canvas.create_image(knight.x, knight.y, image=knight.photo)

    current_drago = 0
    dragon_to_kill = -1

    for dragon in dragons:
        canvas.create_image(dragon.x, dragon.y,  image=dragon.photo)
        dragon.x -= dragon.v

        if ((dragon.x - knight.x) ** 2 + (dragon.y - knight.y) ** 2) ** 0.5 <= 60:
            dragon_to_kill = current_drago

        current_drago += 1

        if dragon.x <=0:
            canvas.delete('all')
            canvas.create_text(width//2, height//2, text='You lose', font=('arial', 54), fill='red')
            break
    if dragon_to_kill >= 0:
        del dragons[dragon_to_kill]

    if len(dragons) == 0:
        canvas.delete('all')
        canvas.create_text(width//2, height//2, text='You win', font=('arial', 54), fill='green')
    else:
        window.after(5, game)


window.bind('<Key-Up>', knight.up)
window.bind('<Key-Down>', knight.down)
window.bind('<Key-Right>', knight.right)
window.bind('<Key-Left>', knight.left)
window.bind('<KeyRelease>', knight.stop)

game()
window.mainloop()
