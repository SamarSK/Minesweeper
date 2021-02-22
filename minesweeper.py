import tkinter
import random

def test():
    #in case a mine already exists at that coords
    global x,y
    area=canvas.find_overlapping(5+x,5+y,15+x,15+y)
    if len(area)==1:
        x=int(random.randint(0,n-1))*20
        y=int(random.randint(0,n-1))*20+50
    area=canvas.find_overlapping(5+x,5+y,15+x,15+y)
    if len(area)==1:
        test()
        
def begin(a,b):
    global count,flags,window,canvas,n,k,x,y,hints
    hints=3 #number of hints
    n=a #number of squares per row/column
    k=b #number of mines
    window.destroy()
    count=0 #counts every click
    flags=k #number of remaining flags
    window=tkinter.Tk()
    window.title("Minesweeper")
    canvas=tkinter.Canvas(width=n*20,height=n*20+50,bg="white")
    canvas.pack()

    for i in range(k):#creates mines
        x=int(random.randint(0,n-1))*20
        y=int(random.randint(0,n-1))*20+50
        test()
        canvas.create_oval(5+x,5+y,15+x,15+y,fill="black")

    canvas.create_rectangle(2,50,n*20,n*20+50,fill="gray65",tags="shroud")#to hide mines

    for i in range(1,n):#creates squares
        canvas.create_line(0,50+i*20,n*20,50+i*20)
        canvas.create_line(i*20,50,i*20,n*20+50)
 
    canvas.create_rectangle(1,51,19,69,outline="red",tags="cursor") #creates cursor

    canvas.create_rectangle(n*10-20,5,n*10,25,fill="lightgrey",width=2)#creates flag counter
    canvas.create_text(n*10-10,15,text=str(flags),fill="red",font="Arial 13",tags="flag")

    canvas.create_rectangle(n*10+10,5,n*10+30,25,fill="lightgrey",width=2)#creates hint counter
    canvas.create_text(n*10+20,15,text=str(hints),fill="green",font="Arial 13",tags="hints")

    canvas.bind_all("<Motion>",movement)
    canvas.bind_all("<Key-h>",hint)
    canvas.bind_all("<Button-1>",firstclick)
    canvas.bind_all("<Button-3>",flag)  

    add_buttons()  

def add_buttons():
    tkinter.Button(command=easy,text="Easy",width=20).pack()
    tkinter.Button(command=med,text="Medium",width=20).pack()
    tkinter.Button(command=hard,text="Hard",width=20).pack()

def easy():
    begin(9,10)   

def med():
    begin(16,40)

def hard():
    begin(22,99)


###################################################################

def movement(f):
    x=f.x
    y=f.y
    if y>50:   
        a=canvas.coords("cursor")
        movex=(x-a[0]-10)/20
        movey=(y-a[1]-10)/20
        canvas.move("cursor",round(movex)*20,round(movey)*20)



def repeat():
    #when on square with no mines around
    #uncovers adjacent squares
    canvas.move("cursor",20,0)
    action(5)
    canvas.move("cursor",-20,0)

    canvas.move("cursor",0,20)
    action(5)
    canvas.move("cursor",0,-20)

    canvas.move("cursor",0,-20)
    action(5)
    canvas.move("cursor",0,20)
    
    canvas.move("cursor",-20,0)
    action(5)
    canvas.move("cursor",20,0)

    canvas.move("cursor",-20,20)
    action(5)
    canvas.move("cursor",20,-20)

    canvas.move("cursor",-20,-20)
    action(5)
    canvas.move("cursor",20,20)

    canvas.move("cursor",20,20)
    action(5)
    canvas.move("cursor",-20,-20)

    canvas.move("cursor",20,-20)
    action(5)
    canvas.move("cursor",-20,20)

def hint(f):
    global hints,n
    if hints>0:
        x=canvas.coords("cursor")
        a=canvas.find_overlapping(x[0],x[1],x[2],x[3])
        if len(a)==2 or len(a)==3:
            for i in a:   #looks if cursor is on mine
                if i in range(1,int(k)+1) or i==p:
                    canvas.create_text(x[0]+9,x[1]+9,text="!",font="Broadway 15",fill="red",tags="sign")
                    canvas.update()
                    canvas.after(500)
                    canvas.delete("sign")
                    hints-=1
                    canvas.delete("hints")
                    canvas.create_text(n*10+20,15,text=str(hints),fill="green",font="Arial 13",tags="hints")
                    return
            canvas.create_text(x[0]+9,x[1]+9,text="✓",font="Broadway 15",fill="green",tags="sign")
            canvas.update()
            canvas.after(500)
            canvas.delete("sign")
            hints-=1
            canvas.delete("hints")
            canvas.create_text(n*10+20,15,text=str(hints),fill="green",font="Arial 13",tags="hints")

def firstclick(f):
    #to ensure that we can't lose on first click
    global x,y,p,n
    p=0
    z=canvas.coords("cursor")
    a=canvas.find_overlapping(z[0],z[1],z[2],z[3])
    if len(a)==3: #if on square with mine
        p=k+2*n+5 #number of "new mine" object
        
        for i in range(k+1,max(canvas.find_overlapping(0,50,n*20,n*20+50))+1):
            canvas.delete(i)

        x=int(random.randint(0,n-1))*20
        y=int(random.randint(0,n-1))*20+50
        test()
        canvas.create_oval(5+x,5+y,15+x,15+y,fill="black")

        canvas.delete(a[0])

        canvas.create_rectangle(2,50,n*20,n*20+50,fill="gray65",tags="shroud")#to hide mines

        for i in range(1,n):#creates squares
            canvas.create_line(0,50+i*20,n*20,50+i*20)
            canvas.create_line(i*20,50,i*20,n*20+50)
 
        canvas.create_rectangle(z[0],z[1],z[2],z[3],outline="red",tags="cursor") #creates cursor
        canvas.bind_all("<Button-1>",action)
        action(5)
    else:
        canvas.bind_all("<Button-1>",action)
        action(5)
        

def action(f):
    #uncovers a square
    global k,n,count,p
    colors=("white","blue","green","red","navy","brown","turquoise","black","grey")
    num=0
    x=canvas.coords("cursor")
    a=canvas.find_overlapping(x[0],x[1],x[2],x[3])#number of objects in cursor area
    if len(a)==2: #if on square without mine
        count+=1
        b=canvas.find_overlapping(x[0]-20,x[1]-20,x[2]+20,x[3]+20)
        for i in b:
            if i in range(1,int(k)+1) or i==p:
                num+=1
        if num==0:
            canvas.create_rectangle(x[0],x[1],x[2],x[3],fill="white",outline="")
            canvas.create_text(x[0]+9,x[1]+9,text=" ",font="Arial 10")
            repeat()
        else:
            canvas.create_rectangle(x[0],x[1],x[2],x[3],fill="white",outline="")
            canvas.create_text(x[0]+9,x[1]+9,text=str(num),font="Broadway 10",fill=colors[num],width=3)

    if len(a)==3: #if on square with mine           
        for i in a:    
            if i in range(1,int(k)+1) or i==p:
                canvas.delete("shroud")
                canvas.delete("cursor")
                canvas.create_rectangle(2,50,n*20,n*20+50)
                canvas.unbind_all("<Button-1>")
                canvas.unbind_all("<Button-3>")
                canvas.unbind_all("<Motion>")
                canvas.unbind_all("<Key-h>")

    if count>=n*n: 
        s=2*n+k+(k*3)+(n*n-k)+(n*n-k)#number of objects if we won
        c=canvas.find_overlapping(0,50,n*20,n*20+50)#current number of objects
        if len(c)==s:
            canvas.create_rectangle(0,0,n*20,50,fill="grey")
            text=canvas.create_text(n*10,25,text="You won!!!",font="Broadway 15",fill="gold")
            canvas.delete("cursor")
            canvas.unbind_all("<Button-1>")
            canvas.unbind_all("<Button-3>")
            canvas.unbind_all("<Motion>")
            canvas.unbind_all("<Key-h>")

def flag(f):
    #draws flag/deletes flag
    global count,n,k,flags,p
    x=canvas.coords("cursor")
    a=canvas.find_overlapping(x[0],x[1],x[2],x[3]) #number of objects in cursor area
    
    if len(a)==5 or len(a)==6: #if flag is on a square, delete it
        canvas.delete(a[-1],a[-2],a[-3])
        flags+=1
        canvas.delete("flag")
        canvas.create_text(n*10-10,15,text=str(flags),fill="red",font="Arial 13",tags="flag")
        
    elif len(a)==2 and flags>0: #if on square without mine, draw flag
        count+=1
        flags-=1
        canvas.create_polygon(x[0]+5,x[1]+2,x[0]+15,x[1]+7,x[0]+5,x[1]+10,fill="red",outline="black")
        canvas.create_line(x[0]+5,x[1]+2,x[0]+5,x[1]+17)
        canvas.create_line(x[0]+5,x[1]+2,x[0]+5,x[1]+17)
        canvas.delete("flag")
        canvas.create_text(n*10-10,15,text=str(flags),fill="red",font="Arial 13",tags="flag")
        

    elif len(a)==3 and flags>0: #if on square with mine or number
        for i in range(0,k+1):
            if i in a or p in a: #if there is mine on square, draw flag (else there is number and we don't draw flag)
                count+=1
                flags-=1
                canvas.create_polygon(x[0]+5,x[1]+2,x[0]+15,x[1]+7,x[0]+5,x[1]+10,fill="red",outline="black")
                canvas.create_line(x[0]+5,x[1]+2,x[0]+5,x[1]+17)
                canvas.create_line(x[0]+5,x[1]+2,x[0]+5,x[1]+17)
                canvas.delete("flag")
                canvas.create_text(n*10-10,15,text=str(flags),fill="red",font="Arial 13",tags="flag")
                if p in a:
                    break
                
    if count>=n*n:
        s=2*n+k+(k*3)+(n*n-k)+(n*n-k) #number of objects if we won
        c=canvas.find_overlapping(0,50,n*20,n*20+50)#current number of objects
        if len(c)==s:
            canvas.create_rectangle(0,0,n*20,50,fill="grey")
            text=canvas.create_text(n*10,25,text="You won!!!",font="Broadway 15",fill="gold")
            canvas.delete("cursor")
            canvas.unbind_all("<Button-1>")
            canvas.unbind_all("<Button-3>")
            canvas.unbind_all("<Motion>")
            canvas.unbind_all("<Key-h>")

          
window=tkinter.Tk()
window.title("Minesweeper")
canvas=tkinter.Canvas(width=0,height=0,bg="white")
canvas.pack()

add_buttons()

tkinter.mainloop()








    


    





    


    


