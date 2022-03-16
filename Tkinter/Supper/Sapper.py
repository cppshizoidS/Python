import tkinter as tk

class MyButton(tk.Button):

    def __init__(self, master, x, y, *args, **kwargs):
        super(MyButton, self).__init__(master, *args, **kwargs)
        self.x = x
        self.y = y
        self.is_mine = False

    def __repr__(self):
        return f'MyButton{self.x} {self.y}'


class Sapper:
    window = tk.Tk()
    ROW = 10
    COLUMNS = 7

    def __init__(self):
        self.buttons = []
        for i in range(Sapper.ROW):
            temp = []
            for j in range(Sapper.COLUMNS):
                btn = MyButton(Sapper.window, x=i, y=j, width=3, font='Arial 15 bold')
                temp.append(btn)
            self.buttons.append(temp)

    def create_widgets(self):
        for i in range(Sapper.ROW):
            for j in range(Sapper.COLUMNS):
                btn = self.buttons[i][j]
                btn.grid(row=i, column=j)

    def start(self):
        self.create_widgets()
        self.print_buttons()
        Sapper.window.mainloop()

    def print_buttons(self):
        for row_btn in self.buttons:
            print(row_btn)


game = Sapper()
game.start()
