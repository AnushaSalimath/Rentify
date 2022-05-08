from tkinter import *
from tkinter import ttk,messagebox
from PIL import ImageTk
import mysql.connector as my
import hostmainwindow
class hostwindow:
    def __init__(self):
        root = Tk()
        self.root = root
        self.root.title("Rentify (HOST)")
        self.root.geometry("1199x600")
        self.root.resizable(False,False)
        self.bg=ImageTk.PhotoImage(file = "download.jpg")
        self.bf_Image= Label(self.root,image = self.bg).place(x = 0,y = 0,relwidth=1,relheight=1)
        
        Framelogin = Frame (self.root,bg = "white")
        Framelogin.place(x = 600,y = 150,height=340,width=500)
        
        title = Label(Framelogin,text = "LOGIN",font= ("Impact",35,"bold"),bg ="#fff",fg="#D77337").place(x = 90,y = 30)
        Desc= Label(Framelogin,text = "LOGIN FOR THE HOST",font= ("Goudy old style",15,"bold"),bg ="#fff",fg="#D25d17").place(x = 90,y = 100)
        username_label = Label(Framelogin,text = "Phone no",font= ("Goudy old style",15,"bold"),bg ="#fff",fg="gray").place(x = 90,y = 140)
        self.txt_user= Entry(Framelogin)
        self.txt_user.place(x = 90, y = 170,width=350,height=35)
        password_label = Label(Framelogin,text = "Aadhar card number",font= ("Goudy old style",15,"bold"),bg ="#fff",fg="gray").place(x = 90,y = 210)
        self.txt_pass = Entry(Framelogin,font = ("times",15))
        self.txt_pass.place(x = 90, y = 240,width=350,height=35)
        login_btn = Button(self.root,text = "Login",bg = "#d77337",fg = "white",font = ("times new roman", 20),command=self.login).place(x = 750,y =470,width=180,height=40)
        
    def run(self):
        self.root.mainloop()
    def login(self):
        if self.txt_pass.get() =="" or self.txt_user == "":
            messagebox.showerror("ERROR","Fields can't be empty!")
        else:
            db = my.connect(
                host = "127.0.0.1",
                user = "root",
                password = "nush2830",
                database = "rentify"
            )
            cursor = db.cursor()
            passe = self.txt_pass.get()
            sql = "SELECT * FROM owner_details WHERE Aadharcard = '{}'".format(passe)
            cursor.execute(sql)
            res = cursor.fetchall()
            if len(res) > 0:
                self.root.destroy()
                obj = hostmainwindow.hostwin(passe)
                obj.run()
            else:
                messagebox.showerror("ERROR","User doesnt exist!!")
        
obj = hostwindow()
obj.run()