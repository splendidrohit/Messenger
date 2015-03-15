from Tkinter import *
from socket import *
import thread
from sys import *

s=socket()
conn=[]
key=0
host='192.168.43.75'
port=5000
root=Tk()
addr=''
f1=Frame(root)
f1.pack()
Label(f1,text='Welcome Rohit....').pack(side=LEFT)
start=Button(f1,text='start server',command=(lambda:init(start,f1)))
start.pack(side=RIGHT)
f=LabelFrame(root)
f.pack()
l1=LabelFrame(f)
l1.pack(side=LEFT)
l2=LabelFrame(f)
l2.pack(side=RIGHT)

Label(l1,text='Send Information to clients').pack()
info=Text(l1,width=20,height=5)
info.pack()
def send():
	msg_info=info.get(0.0,END)
	msg_info='info:>0:>'+msg_info
	info.delete(0.0,END)
	for i in range(key):
		if(conn[i] is not None):
			conn[i][0].send(msg_info)
Button(l1,text='send',command=send).pack()

sc=Scrollbar(l2)
sc.pack(side=RIGHT,fill=Y)
sc2=Scrollbar(l2,orient=HORIZONTAL)
sc2.pack(side=BOTTOM,fill=X)
Label(l2,text='Online clients').pack()
clients=Listbox(l2,width=30,height=10,xscrollcommand=sc2.set,yscrollcommand=sc.set)
clients.pack()
sc.config(command=clients.yview)
sc2.config(command=clients.xview)

def online(c):
	for i in range(c-1):
		if(conn[i] is not None):
			text='add:>'+str(conn[c-1][1])+':> '+conn[c-1][2]
			conn[i][0].send(text)
	if(c==1):
		return
	text='addmany:>'+str(c-1)+':> '
	for i in range(c-1):
		if(conn[i] is not None):
			text=text+conn[i][2]+':'+str(conn[i][1])+': '
	conn[c-1][0].send(text)
	
	
def func(c,sender=key):
	global clients,key,addr
	while True:
		data=c.recv(1024)
		m,no,l=data.split(':>',2)
		if(m=='info'):
			x=[c,key,no]
			c.send('mykey:>'+str(key)+':>'+' ')
			sender=key
			conn.append(x)
			key+=1
			online(key)
			clients.insert(END,l+' , '+no+' , '+str(addr[0])+' :'+str(addr[1]))
			
		elif(m=='info2'):
			for i in range(key):
				if(conn[i] is not None):
					conn[i][0].send(data)
		elif(m=='logout'):
			clients.delete(int(no))
			clients.insert(int(no),conn[int(no)][2]+' gone..')
			conn[int(no)]=None
			for i in range(key):
				if(conn[i] is not None):
					conn[i][0].send(data)
			break
			
		else:
			data=m+':>'+str(sender)+':>'+l
			conn[int(no)][0].send(data)

def add_conn():
	global key,addr
	while True:
		conn1,addr=s.accept()
		thread.start_new_thread(func,(conn1,))
		
		
def init_thread():	
	try:
		thread.start_new_thread(add_conn,())
	except:
		print "can't start thread"
def destroy():
	for i in range(key):
		if(conn[i] is not None):
			conn[i][0].send('destroy:>bye:>Server is closed')
	
	s.close()	
	exit(0)
def close():
	wid=Toplevel()
	wid.grab_set()
	Label(wid,text='Really want to exit').pack()
	f=Frame(wid)
	f.pack()
	Button(f,text='yes',command=destroy).pack(side=LEFT)
	Button(f,text='no',command=wid.destroy).pack(side=RIGHT)
def init(v,f1):
	global s	
	s.bind((host,port))
	s.listen(100)
	v.pack_forget()
	Button(f1,text='close server',command=close).pack(side=RIGHT)
	init_thread()
def cancel():
	return
root.protocol('WM_DELETE_WINDOW',cancel)
root.mainloop()
