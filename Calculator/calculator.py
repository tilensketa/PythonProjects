import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.font import Font
from math import sqrt

root = ttk.Window(title="Calculator", themename="vapor", size=(500, 750), position=(710, 140), resizable=(False, False))
frame = ttk.Frame(root, width=490, height=740)
frame.place(relx=0.5, rely=0.05, anchor=N)

button_font = Font(family="Arial", size=20)
entry_font = Font(family="Arial", size=25, weight="bold")
history_font = Font(family="Arial", size=15)
s = ttk.Style()
s.configure("my.TButton", font=button_font)

button_width = 4
button_pady = 2
button_ipady = 10

def insert_num(num):
    current_num = calculator_entry.get()
    calculator_entry.delete(0, END)
    calculator_entry.insert(0, current_num+str(num))

def insert_operator(operator):
    current_num = calculator_entry.get()
    calculator_entry.delete(0, END)
    calculator_entry.insert(0, current_num+str(operator))

def clear_all():
    calculator_entry.delete(0, END)
    history_label.config(text="")

def clear():
    calculator_entry.delete(0, END)

def calculate():
    equation = calculator_entry.get()
    result = eval(equation)
    calculator_entry.delete(0, END)
    calculator_entry.insert(0, result)
    history_label.config(text=equation+"=")

def delete():
    expression = calculator_entry.get()
    calculator_entry.delete(0, END)
    lista = []
    for digit in expression:
        lista.append(digit)
    if len(lista) != 0:
        lista.pop()
        expression1 = "".join(lista)
        calculator_entry.insert(0, expression1)
    else:
        pass

def square_root():
    number = calculator_entry.get()
    calculator_entry.delete(0, END)
    x = number.isnumeric()
    if x == True:
        calculator_entry.insert(0, "sqrt("+number+")")
        equation = calculator_entry.get()
        result = eval(equation)
        calculator_entry.delete(0, END)
        calculator_entry.insert(0, result)
        history_label.config(text=equation+"=")
    else:
        calculator_entry.insert(0, "error")

def divide_x():
    number = calculator_entry.get()
    calculator_entry.delete(0, END)
    x = number.isnumeric()
    if x == True:
        calculator_entry.insert(0, "1/("+number+")")
        equation = calculator_entry.get()
        result = eval(equation)
        calculator_entry.delete(0, END)
        calculator_entry.insert(0, result)
        history_label.config(text=equation+"=")
    else:
        calculator_entry.insert(0, "error")

def power_2():
    number = calculator_entry.get()
    calculator_entry.delete(0, END)
    x = number.isnumeric()
    if x == True:
        calculator_entry.insert(0, number+"**2")
        equation = calculator_entry.get()
        result = eval(equation)
        calculator_entry.delete(0, END)
        calculator_entry.insert(0, result)
        history_label.config(text=equation+"=")
    else:
        calculator_entry.insert(0, "error")

def percent():
    number = calculator_entry.get()
    calculator_entry.delete(0, END)
    x = number.isnumeric()
    if x == True:
        calculator_entry.insert(0, number+"/100")
        equation = calculator_entry.get()
        result = eval(equation)
        calculator_entry.delete(0, END)
        calculator_entry.insert(0, result)
        history_label.config(text=equation+"=")
    else:
        calculator_entry.insert(0, "error")

def plus_minus():
    number = calculator_entry.get()
    if number != "":
        if number[0] == "-":
            is_minus = True
        else:
            is_minus = False
        if is_minus == False:
            calculator_entry.insert(0, "-")
            is_minus = True
        else:
            equation = calculator_entry.get()
            calculator_entry.delete(0, END)
            equation2 = equation[1:]
            calculator_entry.insert(0, equation2)
            is_minus = False
    else:
        calculator_entry.insert(0, "error")

history_label = ttk.Label(frame, text="", anchor="e", width=25, font=history_font)
history_label.grid(row=0, column=0, columnspan=4, padx=2)

calculator_entry = ttk.Entry(frame, justify="right",width=16, font=entry_font)
calculator_entry.grid(row=1, column=0, columnspan=4, padx=2, ipady=15, pady=button_pady)

button_percent = ttk.Button(frame, text="%", width=button_width, style="my.TButton", command=percent)
button_CE = ttk.Button(frame, text="CE", width=button_width, style="my.TButton", command=clear)
button_C = ttk.Button(frame, text="C", width=button_width, style="my.TButton", command=clear_all)
button_delete = ttk.Button(frame, text="<<", width=button_width, style="my.TButton", command=delete)

button_1_x = ttk.Button(frame, text="1/x", width=button_width, style="my.TButton", command=divide_x)
button_x_2 = ttk.Button(frame, text="x²", width=button_width, style="my.TButton", command=power_2)
button_sqrt_x = ttk.Button(frame, text="√ ̅x", width=button_width, style="my.TButton", command=square_root)
button_division = ttk.Button(frame, text="/", width=button_width, style="my.TButton", command=lambda: insert_operator("/"))

button_7 = ttk.Button(frame, text="7", width=button_width, style="my.TButton", command=lambda: insert_num(7))
button_8 = ttk.Button(frame, text="8", width=button_width, style="my.TButton", command=lambda: insert_num(8))
button_9 = ttk.Button(frame, text="9", width=button_width, style="my.TButton", command=lambda: insert_num(9))
button_multiplication = ttk.Button(frame, text="x", width=button_width, style="my.TButton", command=lambda: insert_operator("*"))

button_4 = ttk.Button(frame, text="4", width=button_width, style="my.TButton", command=lambda: insert_num(4))
button_5 = ttk.Button(frame, text="5", width=button_width, style="my.TButton", command=lambda: insert_num(5))
button_6 = ttk.Button(frame, text="6", width=button_width, style="my.TButton", command=lambda: insert_num(6))
button_subtraction = ttk.Button(frame, text="-", width=button_width, style="my.TButton", command=lambda: insert_operator("-"))

button_1 = ttk.Button(frame, text="1", width=button_width, style="my.TButton", command=lambda: insert_num(1))
button_2 = ttk.Button(frame, text="2", width=button_width, style="my.TButton", command=lambda: insert_num(2))
button_3 = ttk.Button(frame, text="3", width=button_width, style="my.TButton", command=lambda: insert_num(3))
button_addition = ttk.Button(frame, text="+", width=button_width, style="my.TButton", command=lambda: insert_operator("+"))

button_plus_minus = ttk.Button(frame, text="+/-", width=button_width, style="my.TButton", command=plus_minus)
button_0 = ttk.Button(frame, text="0", width=button_width, style="my.TButton", command=lambda: insert_num(0))
button_dot = ttk.Button(frame, text=",", width=button_width, style="my.TButton", command=lambda: insert_operator("."))
button_equals = ttk.Button(frame, text="=", width=button_width,style="my.TButton", command=calculate)

button_percent.grid(row=2, column=0, pady=button_pady, ipady=button_ipady)
button_CE.grid(row=2, column=1, pady=button_pady, ipady=button_ipady)
button_C.grid(row=2, column=2, pady=button_pady, ipady=button_ipady)
button_delete.grid(row=2, column=3, pady=button_pady, ipady=button_ipady)

button_1_x.grid(row=3, column=0, pady=button_pady, ipady=button_ipady)
button_x_2.grid(row=3, column=1, pady=button_pady, ipady=button_ipady)
button_sqrt_x.grid(row=3, column=2, pady=button_pady, ipady=button_ipady)
button_division.grid(row=3, column=3, pady=button_pady, ipady=button_ipady)

button_7.grid(row=4, column=0, pady=button_pady, ipady=button_ipady)
button_8.grid(row=4, column=1, pady=button_pady, ipady=button_ipady)
button_9.grid(row=4, column=2, pady=button_pady, ipady=button_ipady)
button_multiplication.grid(row=4, column=3, pady=button_pady, ipady=button_ipady)

button_4.grid(row=5, column=0, pady=button_pady, ipady=button_ipady)
button_5.grid(row=5, column=1, pady=button_pady, ipady=button_ipady)
button_6.grid(row=5, column=2, pady=button_pady, ipady=button_ipady)
button_subtraction.grid(row=5, column=3, pady=button_pady, ipady=button_ipady)

button_1.grid(row=6, column=0, pady=button_pady, ipady=button_ipady)
button_2.grid(row=6, column=1, pady=button_pady, ipady=button_ipady)
button_3.grid(row=6, column=2, pady=button_pady, ipady=button_ipady)
button_addition.grid(row=6, column=3, pady=button_pady, ipady=button_ipady)

button_plus_minus.grid(row=7, column=0, pady=button_pady, ipady=button_ipady)
button_0.grid(row=7, column=1, pady=button_pady, ipady=button_ipady)
button_dot.grid(row=7, column=2, pady=button_pady, ipady=button_ipady)
button_equals.grid(row=7, column=3, pady=button_pady, ipady=button_ipady)

def update_scale(self):
    number = dark_light_theme_scale.get()
    if number < 0.5:
        s.theme_use("vapor")
        dark_light_theme_scale.set(0)
    else:
        s.theme_use("litera")
        e = ttk.Style()
        e.configure("my.TButton", font=button_font)
        dark_light_theme_scale.set(1)

dark_light_theme_scale = ttk.Scale(frame, length=5, from_=0, to=1, cursor="hand2")
dark_light_theme_scale.grid(row=8, column=0, pady=20)

dark_light_theme_scale.bind("<ButtonRelease-1>", update_scale)

root.mainloop()