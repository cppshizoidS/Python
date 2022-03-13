import tkinter as tk
from tkinter import messagebox


def add_digit(digit):
    value = calc.get()
    if value[0]=='0' and len(value)==1:
        value = value[1:]
    calc['state']=tk.NORMAL
    calc.delete(0,tk.END)
    calc.insert(0,value+digit)
    calc['state'] = tk.DISABLED

def add_operation(operation):
    value = calc.get()
    if value[-1] in '-+/*':
        value = value[:-1]
    elif '+' in value or '-' in value or '*' in value or '/' in value:
        calculate()
        value = calc.get()
    calc['state'] = tk.NORMAL
    calc.delete(0, tk.END)
    calc.insert(0, value+operation)
    calc['state'] = tk.DISABLED

def calculate():
    value = calc.get()
    if value[-1] in '+-/*':
        operation = value[-1]
        value = value[:-1]+operation+value[:-1]
    calc['state'] = tk.NORMAL
    calc.delete(0, tk.END)
    try:
        calc.insert(0, eval(value))
    except (NameError,SyntaxError):
        messagebox.showinfo('Warning', 'Only numbers and operators')
        calc.insert(0, 0)
    except ZeroDivisionError:
        messagebox.showinfo('Warning', 'Zero Division')
        calc.insert(0, 0)


def clear():
    calc.delete(0, tk.END)
    calc.insert(0,0)

def make_digit_button(digit):
    return tk.Button(text=digit, bd=5, font=('Arial', 13), command=lambda: add_digit(digit))

def make_operation_button(operation):
    return tk.Button(text=operation, bd=5, font=('Arial', 13), fg='red', command=lambda: add_operation(operation))

def make_calc_button(operation):
    return tk.Button(text=operation, bd=5, font=('Arial', 13), fg='red', command=calculate)

def make_clear_button(operation):
    return tk.Button(text=operation, bd=5, font=('Arial', 13), fg='red', command=clear)

def press_key(event):
    print(repr(event.char))
    if event.char.isdigit():
        add_digit(event.char)
    elif event.char in '+-*/':
        add_operation(event.char)
    elif event.char == '\r':
        calculate()

win = tk.Tk()
win.geometry(f"240x260+100+200")
win['bg'] = '#33FFE6'
win.title('Calculator')

win.bind('<Key>', press_key)

calc = tk.Entry(win, justify=tk.RIGHT, font= ('Arial', 15), width= 15)
calc.insert(0,'0')
calc['state'] = tk.DISABLED
calc.grid(row=0, column=0, columnspan=4, stick='we', padx=5)

make_digit_button('1').grid(row = 1, column=0,stick='wens',padx =5, pady = 5)
make_digit_button('2').grid(row = 1, column=1,stick='wens',padx =5, pady = 5)
make_digit_button('3').grid(row = 1, column=2,stick='wens',padx =5, pady = 5)
make_digit_button('4').grid(row = 2, column=0,stick='wens',padx =5, pady = 5)
make_digit_button('5').grid(row = 2, column=1,stick='wens',padx =5, pady = 5)
make_digit_button('6').grid(row = 2, column=2,stick='wens',padx =5, pady = 5)
make_digit_button('7').grid(row = 3, column=0,stick='wens',padx =5, pady = 5)
make_digit_button('8').grid(row = 3, column=1,stick='wens',padx =5, pady = 5)
make_digit_button('9').grid(row = 3, column=2,stick='wens',padx =5, pady = 5)
make_digit_button('0').grid(row = 4, column=1,stick='wens',padx =5, pady = 5)

make_operation_button('+').grid(row = 1, column=3,stick='wens',padx =5, pady = 5)
make_operation_button('-').grid(row = 2, column=3,stick='wens',padx =5, pady = 5)
make_operation_button('*').grid(row = 3, column=3,stick='wens',padx =5, pady = 5)
make_operation_button('/').grid(row = 4, column=3,stick='wens',padx =5, pady = 5)
make_calc_button('=').grid(row = 4, column=2, stick='wens',padx =5, pady = 5)
make_clear_button('C').grid(row = 4, column=0, stick='wens',padx =5, pady = 5)



win.grid_columnconfigure(0,minsize=52)
win.grid_columnconfigure(1,minsize=52)
win.grid_columnconfigure(2,minsize=52)
win.grid_columnconfigure(3,minsize=52)


win.grid_rowconfigure(0,minsize=52)
win.grid_rowconfigure(1,minsize=52)
win.grid_rowconfigure(2,minsize=52)

win.mainloop()
