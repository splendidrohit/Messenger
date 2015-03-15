from Tkinter import *
from socket import *
import thread
from sys import *

host=gethostname()
id='192.168.43.75'
#id=host
conn=socket()
port=5000
main=Tk()
Label(main,text='BeeChat',font=('times',25,'bold'),bg='brown',fg='antique white').pack(fill=X,expand=1)
root=Frame(main)
root.pack()
mykey=0
myname=[]
#variables..
online=[]
left=None
right=None
l2=None
p=None
mainl=None
info=None
info2=None
comm=None


class user(LabelFrame):
    def __init__(self,parent,name,id=None):
        self.parent=parent
        self.show=False
        LabelFrame.__init__(self,parent)
        self.name=name
        self.id=id
        self.title=Label(self,text=name)
        self.title.pack(fill=BOTH,expand=1)
        self.scrollbar = Scrollbar(self) 
        self.scrollbar.pack( side = RIGHT, fill=Y )
        self.view=Text(self,state=DISABLED,yscrollcommand=self.scrollbar.set,width=21,height=15)
        self.scrollbar.config(command=self.view.yview)
        self.view.pack()
        self.view.pack_propagate(0)
    
        
        self.f=Frame(self)
        self.f.pack()
        self.write=Entry(self.f,width=20)
        self.write.pack(side=LEFT)
        self.write.bind('<Return>',self.gettext)
        Button(self.f,text='send',command=self.gettext).pack(side=RIGHT)
        self.view.config(font=('courier', 10, 'bold'))
        
        
    def gettext(self,event=None):
        global conn
        msg=self.write.get()
        self.write.delete(0,END)
        if(msg is not ""):
            self.add_msg('< '+msg)
            msg='text:>'+self.id+':>'+msg
            conn.send(msg)
        
           
    def add_msg(self,msg):
        self.view.config(state=NORMAL)
        self.view.insert(INSERT,msg+'\n')
        self.view.config(state=DISABLED)
def hataor(v):
    global left,right
    left.pack_forget()
    left.show=False
    v.pack(side=LEFT)
    left=right
    right=v
    v.show=True
    
def hatao(v):
    v.pack_forget()
        
def draw(v):
                global left,right
                if(left is None and right is None):
                    v.pack(side=LEFT)
                    left=v
                    v.show=True
                elif(left is not None and right is None):
                    v.pack(side=LEFT)
                    right=v
                    v.show=True
                elif(left is not None and right is not None):
                    main.after(10,lambda:hataor(v))
                    
                
                

def handle(event):
    global p
    index = p.curselection()
    if(online[int(index[0]>=0) and int(index[0])][0].show==False ):
            draw(online[int(index[0])][0])
            online[int(index[0])][0].show=True
  

def get_message():
    global l2,online,p
    while True:
         t=conn.recv(1024)
         order,id,msg=t.split(':>',2)
         if(order == "add"):
            x=user(l2,msg,id)
            m=(x,id)
            online.append(m)
            p.insert(END,msg)
            
         elif(order == "text"):
                 global var
                 for i in online:
                    if(i[1] is id):
                        var=i[0]
                        main.after(10,(lambda:i[0].add_msg(' > '+msg)))
                        if(i[0].show==False):
                            draw(i[0])  
                                  
                        break           
         elif(order=="addmany"):
                n=int(id)         
                for i in range(n):
                     if(msg==' '):
                         break
                     name,id,msg=msg.split(':',2)
                     x=user(l2,name,id)
                     m=(x,id)
                     online.append(m)
                     p.insert(END,name)
         elif(order=="info"):
            global info
            info.config(text='\n'+msg+'\n')
         elif(order=="info2"):
            global info2
            info2.config(state=NORMAL)
            info2.insert(END,id+' :>  '+msg)
            info2.config(state=DISABLED)
         elif(order=="destroy"):
            main.after(10,(lambda:hatao(root)))
            Label(main,text='Server is closed').pack()
            Button(main,text='ok',command=exit).pack()
            break
         elif(order=='mykey'):
            global mykey
            mykey=int(id)
         elif(order=='logout'):
            temp=int(id)
            global right
            for i in range(len(online)):
                if(temp is int(online[i][0].id)):
                    if(online[i][0].show==True):
                        tempi=online[i][0]
                        main.after(10,(lambda:hatao(tempi)))
                        right=None
                    online[i]=None
                    online.remove(online[i])
                    p.delete(i)
                    break
        


  
def proceed(name1,name2,wid):
        global myname,host,mainl
        myname.append(name1)
        myname.append(name2)
        if(name1=='' or name2==''):
            return
        name=name1+' '+name2
        mainl.config(text='Welcome '+name1)
        info='info:>'+name+':>'+host
        conn.send(info)
        wid.destroy()
    
def cancel():
    return   
def make_wid():
    wid=Toplevel()
    wid.protocol('WM_DELETE_WINDOW',cancel)
    tf=Frame(wid)
    tf.pack()
    wid.grab_set()
    wid.resizable(0,0)
    Label(tf,text='Your Name').pack(side=LEFT)
    name1=Entry(tf)
    name2=Entry(tf)
    name1.pack(side=LEFT)
    name2.pack(side=RIGHT)
    Button(wid,text='proceed',command=(lambda:proceed(name1.get(),name2.get(),wid))).pack()


def send_command(event=None):
    global comm
    c=comm.get(0.0,END)
    comm.delete(0.0,END)
    c='info2:>'+myname[0]+':>'+c
    conn.send(c)
 
def logout_me():
    conn.send('logout:>'+str(mykey)+':>'+'check')
    conn.close()
    exit(0)
 
def logout():
    wid=Toplevel()
    wid.grab_set()
    Label(wid,text='Do u really want to exit').pack()
    f=Frame(wid)
    f.pack()
    Button(f,text='Yes',command=logout_me).pack(side=LEFT)
    Button(f,text='Cancel',command=wid.destroy).pack(side=RIGHT)
     

def init():
    global p,l2,mainl,info,info2,comm
    try :
        conn.connect((id,port))
        init_fram.pack_forget()
        make_wid()
        ht=300
        wt=200
        word=20
        tf=Frame(root)
        tf.pack(fill=X)
        mainl=Label(tf,text='welcome',anchor='center',font=('times',20,'italic'))
        mainl.pack(side=LEFT,expand=1)
        Button(tf,text='LogOut',command=logout).pack(side=RIGHT)
        f=LabelFrame(root)
        f.pack()
        l1=LabelFrame(f,width=wt,height=ht)
        l1.pack(side=LEFT)
        x=LabelFrame(l1)
        x.pack(fill=X)
        Label(x,text='Message from admin:',font=('times',15,'italic')).pack()
        info=Message(l1,width=200,text='WELCOME FRIENDS...\n\n\n')
        info.pack()
        info.pack_propagate(0)
    
        x1=LabelFrame(l1)
        x1.pack(fill=X)
        sb=Scrollbar(l1)
        Label(x1,text='Your Responses:',font=('times',15,'italic')).pack()
        info2=Text(l1,width=100,state=DISABLED,yscrollcommand=sb.set,font=('courier', 10, 'bold'))
        sb.pack(side=RIGHT,fill=Y)
        
        sb.config(command=info2.yview)
        
        info2.pack()


        l1.pack_propagate(0)
        l2=LabelFrame(f,width=2*wt,height=ht)
        l2.pack(side=LEFT)
        l2.pack_propagate(0)
        f2=LabelFrame(f)
        f2.pack()
        l=Frame(f2)
        l.pack()
        xx=LabelFrame(f2)
        xx.pack()
        Label(l,text='Online Friends',width=word).pack()
        sc=Scrollbar(xx)
        sc.pack(side=RIGHT,fill=Y)
        p=Listbox(xx,width=word,height=10,yscrollcommand=sc.set,relief=SUNKEN)
        sc.config(command=p.yview)
        p.pack()
        p.config(selectmode=SINGLE, setgrid=1)
        p.bind('<Double-1>',handle)
        Label(f2,text='Comment').pack()
        comm=Text(f2,width=20,height=3)
        comm.bind('<Return>',(send_command))
        comm.pack()
        Button(f2,text='send',command=send_command).pack()
        main.protocol('WM_DELETE_WINDOW',cancel)
        thread.start_new_thread(get_message,())
    except:
        pass

init_fram=Frame(root)
init_fram.pack()
Label(init_fram,text='SERVER IS OFF....').pack()
Button(init_fram,text='Retry',command=init).pack()
main.title("Beechat")
main.resizable(0,0)
init()      

main.mainloop()