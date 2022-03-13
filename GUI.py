from tkinter import *

main = Tk()

def button_cliked():
    text = Label(main,text = "button has clicked")
    text.pack()

button_one = Button(main,text="click me", fg='green', highlightbackground='black', command=button_cliked)

button_one.pack()

button_two = Button(main,text="click me", fg='red', highlightbackground='white', command=button_cliked)

button_two.pack(padx= 100, pady= 100)

main.mainloop()

