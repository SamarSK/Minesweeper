import tkinter
import random

ind=0
n=9 #number of squares (16x16)
k=10 #number of mines
count=0
flags=k #number of remaining flags
window=tkinter.Tk()
window.title("Minesweeper")
canvas=tkinter.Canvas(width=n*20,height=n*20+50,bg="white")
canvas.pack()

def boom(f):
    #press Esc to kill the game
    window.destroy()

def flag(f):
    #draws flag/deletes flag
    global count,n,k,flags,ind
    x=canvas.coords("cursor")
    a=canvas.find_overlapping(x[0],x[1],x[2],x[3]) #number of objects in cursor area
    if len(a)>=4: #if flag is on a square, delete it
        canvas.delete(a[-1],a[-2])
        flags+=1
        canvas.delete("flag")
        canvas.create_text(n*10,25,text=str(flags),fill="red",font="Arial 20",tags="flag")
        
    elif len(a)==2 and flags>0: #if on square without mine, draw flag
        count+=1
        flags-=1
        canvas.create_polygon(x[0]+5,x[1]+2,x[0]+15,x[1]+7,x[0]+5,x[1]+10,fill="red",outline="black")
        canvas.create_line(x[0]+5,x[1]+2,x[0]+5,x[1]+17)
        canvas.delete("flag")
        canvas.create_text(n*10,25,text=str(flags),fill="red",font="Arial 20",tags="flag")

    elif len(a)==3: #if on square with mine or number
        for i in range(0,k+1):
            if i in a: #if there is mine on square, draw flag (else there is number and we don't draw flag)
                count+=1
                flags-=1
                canvas.create_polygon(x[0]+5,x[1]+2,x[0]+15,x[1]+7,x[0]+5,x[1]+10,fill="red",outline="black")
                canvas.create_line(x[0]+5,x[1]+2,x[0]+5,x[1]+17)
                canvas.delete("flag")
                canvas.create_text(n*10,25,text=str(flags),fill="red",font="Arial 20",tags="flag")

    if count>=n*n:
        s=2*n+k+(k*2)+(n*n-k) #number of objects if we won
        c=canvas.find_overlapping(0,50,n*20,n*20+50)#current number of objects
        if len(c)==s:
            ind=1
            canvas.create_rectangle(0,0,n*20,50,fill="grey")
            text=canvas.create_text(n*10,25,text="You won!!!",font="Broadway 15",fill="gold")
            canvas.delete("cursor")
            
    
def test():
    #in case a mine already exists at that coords
    global x,y
    area=canvas.find_overlapping(5+x,5+y,15+x,15+y)
    if str(area)[1]!=")":
        x=int(random.randint(0,n-1))*20
        y=int(random.randint(0,n-1))*20+50
    area=canvas.find_overlapping(5+x,5+y,15+x,15+y)
    if str(area)[1]!=")":
        test()

def action(f):
    #uncovers a square
    global k,n,count,ind
    colors=["white","blue","green","red","navy","brown","turquoise","black","grey"]
    num=0
    x=canvas.coords("cursor")
    a=canvas.find_overlapping(x[0],x[1],x[2],x[3])#number of objects in cursor area
    if len(a)==2: #if on square without mine
        count+=1
        b=canvas.find_overlapping(x[0]-20,x[1]-20,x[2]+20,x[3]+20)
        for i in b:
            if i in range(1,int(k)+1):
                num+=1
        if num==0:
            canvas.create_text(x[0]+9,x[1]+9,text="°",font="Arial 10")
        else:
            canvas.create_text(x[0]+9,x[1]+9,text=str(num),font="Broadway 10",fill=colors[num],width=3)

    if len(a)==3: #if on square with mine           
        for i in a:    
            if i in range(1,int(k)+1):
                ind=1
                canvas.delete("shroud")
                canvas.delete("cursor")
                canvas.create_rectangle(2,50,n*20,n*20+50)

    if count>=n*n: 
        s=2*n+k+(k*2)+(n*n-k)#number of objects if we won
        c=canvas.find_overlapping(0,50,n*20,n*20+50)#current number of objects
        if len(c)==s:
            ind=1
            canvas.create_rectangle(0,0,n*20,50,fill="grey")
            text=canvas.create_text(n*10,25,text="You won!!!",font="Broadway 15",fill="gold")
            canvas.delete("cursor")              
def te(f):
    global ind
    if ind==0:
        x=f.x
        y=f.y
        a=canvas.coords("cursor")
        posunx=(x-a[0]-10)/20
        posuny=(y-a[1]-10)/20
        canvas.move("cursor",round(posunx)*20,round(posuny)*20)
    else:
        return True

for i in range(k):#creates mines
    x=int(random.randint(0,n-1))*20
    y=int(random.randint(0,n-1))*20+50
    test()
    canvas.create_oval(5+x,5+y,15+x,15+y,fill="black")
canvas.create_rectangle(2,50,n*20,n*20+50,fill="white",tags="shroud")#to hide mines

for i in range(1,n):#creates squares
    canvas.create_line(0,50+i*20,n*20,50+i*20)
    canvas.create_line(i*20,50,i*20,n*20+50)

canvas.create_rectangle(1,51,19,69,outline="red",width=3,tags="cursor") #creates cursor

canvas.create_rectangle(n*10-15,10,n*10+15,40,fill="lightgrey",width=2) #creates flag counter
canvas.create_text(n*10,25,text=str(flags),fill="red",font="Arial 20",tags="flag")


canvas.bind_all("<Button-1>",action)
canvas.bind_all("<Button-3>",flag)
canvas.bind_all("<Escape>",boom)
canvas.bind_all("<Motion>",te)



    


    


