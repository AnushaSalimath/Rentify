from logging import captureWarnings
from tkinter import *
from tkinter import messagebox
import mysql.connector as my
from tkinter import ttk
import random
location,owner,Username = "","",""
class mainpage:
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
        sql = "SELECT NAME FROM Users where userid = '{}'".format(self.user)
        cursor.execute(sql)
        result = list(cursor.fetchall())
        Username = result[0][0]
        self.root = root
        self.root.title("Rentify")
        self.root.resizable(False,False)
        self.root.geometry("600x600")
        heading = Label(self.root,text="Rentify",font=("times new roman",34,"bold"))
        heading.place(x = 225,y = 20)
        search = ttk.Button(self.root,text = "Search",command=self.search)
        search.place(x = 20,y=20)
        refresh = ttk.Button(self.root,text = "Refresh",command=self.refersh)
        refresh.place(x = 500,y=20)
        res = ttk.Button(self.root,text = "Response",command=self.res)
        res.place(x = 20,y=60)
        
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
        self.my_tree['columns'] = ("Location","Rent price","Ownername")
        self.my_tree.column("#0",width=0,stretch=NO)
        self.my_tree.column("Location",anchor=W,width=120)
        self.my_tree.column("Rent price",anchor=CENTER,width=80)
        self.my_tree.column("Ownername",anchor=W,width=120)
        
        self. my_tree.heading("#0",text = "",anchor=CENTER)
        self. my_tree.heading("Location",text="Location",anchor=CENTER)
        self. my_tree.heading("Rent price",text = "Rent Price",anchor=CENTER)
        self. my_tree.heading("Ownername",text="Owner name",anchor=CENTER)
        self.my_tree.pack(pady=20)
        tree_scroll.config(command=self.my_tree.yview)
        
        
        
        self.my_tree.tag_configure('oddrow',background="white")
        self.my_tree.tag_configure('evenrow',background="lightblue")
        self.my_tree.bind("<Double-1>",self.select)
        
        self.Location = Label(self.root,text = "Location:")
        self.Location.place(x = 230,y = 410)
        self.Owner = Label(self.root,text = "Owner name:")
        self.Owner.place(x = 230,y = 430)
        self.price = Label(self.root,text = "Price:")
        self.price.place(x = 230,y = 450)
        self.message = Label(self.root,text = "Want to send an confirmation for the booking of this house?")
        self.message.place(x = 150,y = 470)
        send = ttk.Button(self.root,text = "Send Request",command=self.sendrequest)
        send.place(x = 230 , y = 490)
        self.status = Label(self.root,text = "Currently logged in as: "+Username)
        self.status.place(x = 0,y = 570)
    def res(self):
        db = my.connect(
            host = "127.0.0.1",
            user = "root",
            password = "nush2830",
            database = "rentify"
        )
        cursor = db.cursor()
        sql = "SELECT * FROM request WHERE Username = '{}'".format(Username)
        print(Username)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        if len(result) == 0:
            messagebox.showinfo("Status","No request has been submitted by you")
        else:
            reswin = Toplevel()
            reswin.title("Response")
            reswin.geometry("200x200")
            head = Label(reswin,text = "Request id: "+str(result[0][0]))
            head.pack()
            uname = Label(reswin,text = "Name: "+result[0][1])
            uname.pack()
            owner= Label(reswin,text = "Owner name: "+result[0][2])
            owner.pack()
            loc = Label(reswin,text =  "Location: "+result[0][3])
            loc.pack()
            message = Label(reswin,text = "Message: "+result[0][4])
            message.pack()
    def refersh(self):
        self.query()
    def search(self):
        def getrecords():
            record = entry.get()
            window.destroy()
            for records in self.my_tree.get_children():
                self.my_tree.delete(records)
            
            for record in self.my_tree.get_children():
                self.my_tree.delete(record)
            db = my.connect(
                host = "127.0.0.1",
                user = "root",
                password = "nush2830",
                database = "rentify"
            )
            cursor = db.cursor()
            sql = "SELECT * FROM house_details WHERE location like '{}%'".format(record)
            cursor.execute(sql)
            records = cursor.fetchall()
            print(records)
            global count
            count = 0
            
            for rec in records:
                if count%2 == 0:
                    self.my_tree.insert(parent='',index='end',iid=count,text='',values = (rec[1],rec[2],rec[0]),tags=('evenrow',))
                else:
                    self.my_tree.insert(parent='',index='end',iid=count,text='',values = (rec[1],rec[2],rec[0]),tags=('oddrow',))
                count+=1
        
        global entry,window    
        window = Toplevel()
        window.title("Search")
        window.geometry("400x200")
        
        search_frame = LabelFrame(window,text = "Enter your location")
        search_frame.pack(padx=10,pady=10)
        
        entry = ttk.Entry(search_frame,font=("Helvectic",18))
        entry.pack(pady = 20,padx =20)
        but = ttk.Button(window,text = "Search",command=getrecords)
        but.pack(padx = 20,pady =20)
    def sendrequest(self):
        global location,owner,Username
        db = my.connect(
            host = "127.0.0.1",
            user = "root",
            password = "nush2830",
            database ="rentify"
        )
        try:
            cursor = db.cursor()
            reqid = str(random.randint(100000,999999))
            sql1 = "SELECT * FROM request WHERE Username  = '{}' and Message = 'NO'".format(Username)
            cursor.execute(sql1)
            res = cursor.fetchall()
            if len(res) > 0:
                messagebox.showerror("Denied","Your request:{} has not been processed .\nPlease wait till the request gets processed.".format(res[0][0]))
            else:
                sql = "INSERT INTO request values(%s,%s,%s,%s,'NO')"
                val = (reqid,Username,owner,location)
                cursor.execute(sql,val)
                db.commit()
                messagebox.showinfo("Success","Your Request has been Processed.\nRequest id:{}".format(reqid))
        except:
            messagebox.showerror("Error","Could not generate request .Please try again later!")
        
    def select(self,event):
        global location,owner
        item = self.my_tree.selection()[0]
        values = self.my_tree.item(item,'values')
        location = values[0]
        owner = values[2]
        self.Location['text'] = "Location: "+values[0]
        self.Owner['text'] = "Owner name: "+values[2]
        self.price['text'] = "Price: "+values[1]
    def run(self):
        self.root.mainloop() 
         
         
    def stop(self):
        self.root.destroy()
    def query(self):
        for record in self.my_tree.get_children():
            self.my_tree.delete(record)
        db = my.connect(
            host = "127.0.0.1",
            user = "root",
            password = "nush2830",
            database = "rentify"
        )
        cursor = db.cursor()
        sql = "SELECT * FROM house_details"
        cursor.execute(sql)
        records = cursor.fetchall()
        global count
        count = 0
        
        for rec in records:
            if count%2 == 0:
                self.my_tree.insert(parent='',index='end',iid=count,text='',values = (rec[1],rec[2],rec[0]),tags=('evenrow',))
            else:
                self.my_tree.insert(parent='',index='end',iid=count,text='',values = (rec[1],rec[2],rec[0]),tags=('oddrow',))
            count+=1
        
