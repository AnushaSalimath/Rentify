from tkinter import *
from tkinter import ttk,messagebox
import mysql.connector as my
import random

from mysql.connector.errors import custom_error_exception
location,owner,Username = "","",""
reqname = ""
class hostwin:
    def __init__(self,user):
        global Username
        root = Tk()
        self.user = user
        db = my.connect(
            host = "127.0.0.1",
            user = "root",
            password = "nush2830",
            database = "rentify"
        )
        cursor = db.cursor()
        sql = "SELECT Ownername FROM owner_details where Aadharcard  = '{}'".format(self.user)
        cursor.execute(sql)
        result = list(cursor.fetchall())
        Username = result[0][0]
        self.root = root
        self.root.title("Rentify(host)")
        self.root.resizable(False,False)
        self.root.geometry("600x600")
        heading = Label(self.root,text="Rentify",font=("times new roman",34,"bold"))
        heading.place(x = 225,y = 20)
        refresh = ttk.Button(self.root,text = "Refresh",command=self.refersh)
        refresh.place(x = 500,y=20)
        add = ttk.Button(self.root,text = "Add",command=self.add)
        add.place(x = 20,y=20)
        
        style = ttk.Style()
        
        style.configure("Treeview",
                    background = "#D3D3D3",
                    foreground ="black",
                    rowheight = 25,
                    fieldbackground = "#D3D3D3")
        style.map("Treeview",
                background = [('selected',"#347093")])
        tree_frame = Frame(root)
        tree_frame.pack(pady=100)
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side = RIGHT,fill=Y)
        self.my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended")
        self.my_tree['columns'] = ("requestid","Username","Ownername","Location")
        self.my_tree.column("#0",width=0,stretch=NO)
        self.my_tree.column("requestid",anchor=W,width=120)
        self.my_tree.column("Username",anchor=CENTER,width=80)
        self.my_tree.column("Ownername",anchor=W,width=120)
        self.my_tree.column("Location",anchor=W,width=120)
        
        self. my_tree.heading("#0",text = "",anchor=CENTER)
        self. my_tree.heading("requestid",text="Request id",anchor=CENTER)
        self. my_tree.heading("Username",text = "Name",anchor=CENTER)
        self. my_tree.heading("Ownername",text="Owner name",anchor=CENTER)
        self. my_tree.heading("Location",text="Location",anchor=CENTER)
        self.my_tree.pack(pady=20)
        tree_scroll.config(command=self.my_tree.yview)
        
        
        
        self.my_tree.tag_configure('oddrow',background="white")
        self.my_tree.tag_configure('evenrow',background="lightblue")
        self.my_tree.bind("<Double-1>",self.select)
        
        self.Owner = Label(self.root,text = "Name:")
        self.Owner.place(x = 230,y = 410)
        self.message = Label(self.root,text = "Want to send an confirmation for a meeting to the client?")
        self.message.place(x = 150,y = 430)
        send = ttk.Button(self.root,text = "Send Request",command=self.sendrequest)
        send.place(x = 230 , y = 490)
        self.status = Label(self.root,text = "Currently logged in as: "+Username)
        self.status.place(x = 0,y = 570)
        
    def add(self):
        def addrecord():
            db = my.connect(
                host = "127.0.0.1",
                user = "root",
                password = "nush2830",
                database = "rentify"
            )
            cursor = db.cursor()
            sql = "INSERT INTO house_details VALUES(%s,%s,%s)"
            locat = entry.get()
            price = entry1.get()
            val = (Username,locat,price)
            cursor.execute(sql,val)
            db.commit()
        global entry,entry1
        window = Toplevel()
        window.title("Add")
        window.geometry("500x500")

        search_frame = LabelFrame(window,text = "House situated at")
        search_frame.pack(padx=10,pady=10)
        
        entry = ttk.Entry(search_frame,font=("Helvectic",18))
        entry.pack(pady = 20,padx =20)
        entry1 = ttk.Entry(search_frame,font=("Helvectic",18))
        entry1.pack(pady = 20,padx =20)
        but = ttk.Button(window,text = "Add",command=addrecord)
        but.pack(padx = 20,pady =20)
    def refersh(self):
        self.query()
    def sendrequest(self):
        db = my.connect(
            host = "127.0.0.1",
            user ="root",
            password = "nush2830",
            database = "rentify"
        )
        cursor = db.cursor()
        sqlgetno = "SELECT Phoneno FROM owner_details WHERE Ownername = '{}'".format(Username)
        cursor.execute(sqlgetno)
        result = cursor.fetchall()
        print(result)
        message = "Contact me."+str(result[0])
        print(message)
        sql = "UPDATE request SET message = (%s) WHERE Username = (%s)"
        val = (message,reqname)
        cursor.execute(sql,val)
        db.commit()
        messagebox.showinfo("Status","The message has been generated.")
    def select(self,event):
        global reqname
        item = self.my_tree.selection()[0]
        values = self.my_tree.item(item,'values')
        reqname = values[1]
        self.Owner['text'] = "Name: "+values[1]
    def run(self):
        self.root.mainloop()
        
    def stop(self):
        self.root.destroy()
    def query(self):
        global Username
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
        db = my.connect(
            host = "127.0.0.1",
            user = "root",
            password = "nush2830",
            database = "rentify"
        )
        cursor = db.cursor()
        sql = "SELECT * FROM request where Location in (SELECT Address FROM owner_details where Ownername = '{}') and Ownername = '{}' and Message = 'NO'".format(Username,Username)
        cursor.execute(sql)
        records = cursor.fetchall()
        global count
        count = 0
        
        for rec in records:
            if count%2 == 0:
                self.my_tree.insert(parent='',index='end',iid=count,text='',values = (rec[0],rec[1],rec[2],rec[3]),tags=('evenrow',))
            else:
                self.my_tree.insert(parent='',index='end',iid=count,text='',values = (rec[0],rec[1],rec[2],rec[3]),tags=('oddrow',))
            count+=1
