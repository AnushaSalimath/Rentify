import tkinter as tk
from tkinter import *
w=tk.Tk()
tk.var=tk.DoubleVar()

def clickedbutton():
    a=int(text.get())
    b=int(text2.get())
    if a>b:
        text3.insert(tk.END,f"a:{a} is greater than b:{b}")
        bt.config(text="Button clicked")
    elif a<b:
        text3.insert(tk.END,f"a:{a} is smaller than b:{b}")
        bt.config(text="Button clicked")
    else:
        text3.insert(tk.END,f"a: {a} and b: {b} are both equal")
        bt.config(text="Button clicked")
    
def clear():
    text.delete(0,END)
    text2.delete(0,END)
    text3.delete(0,END)

w.geometry('400x200')
l=tk.Label(w,text="NUM1")
l.grid(column=0,row=0)

text=tk.Entry(w,width=10)
text.grid(column=1,row=0)

l2=tk.Label(w,text="NUM2")
l2.grid(column=0,row=1)

text2=tk.Entry(w,width=10)
text2.grid(column=1,row=1)

l3=tk.Label(w,text="Result")
l3.grid(column=0,row=2)

text3=tk.Entry(w,width=40)
text3.grid(column=1,row=2)

bt=tk.Button(w,text="Result",command=clickedbutton)
bt.grid(column=1,row=3)

bt1=tk.Button(w,text="Clear",command=clear)
bt1.grid(column=1,row=4)

w.mainloop()





































