
from collections import deque
import time
import heapq
class Node:
    def __init__(self,s,a=None, p=None, c=0):
        self.state=s
        self.action=a
        self.parent=p
        self.cost=c   #بتفيدنا النود في اي لفل بالتالي بعرف لما الاقي النتيجة هو وين 

    def menhaten(self):
        dis=0
        count=1
        for i in self.state:
            if i != 0:
                d=i-count
                if d==2 or d==-2:
                    dis=dis+2
                elif d==3 or d==-3:
                    dis=dis+1
                elif d==5 or d==-5:
                    dis=dis+3
                elif d==6 or d==-6:
                    dis=dis+2
                elif d==7 or d==-7:
                    dis=dis+3
                elif d==8 or d==-8:
                    dis=dis+4
                elif d==1 and (count==3 or count==6):
                    dis = dis+3
                elif d==-1 and(count==4 or count==7):
                    dis=dis+3
                elif d==1 or d==-1:
                    dis=dis+1
                elif d==4 and(count==3 or count==7):
                    dis=dis+4
                elif d==4 or d==-4:
                    dis=dis+2
            count=count+1
        return dis
    def __lt__(self,other):
        return self.menhaten()<other.menhaten()


class EightPuzzle:
    def __init__(self, istate,c=0,fl=0,fm=1,dm=0):
        self.initial_state=istate
        self.count=c
        self.fringelen = fl
        self.fringemax=fm
        self.depthmax=dm

    def GoalTest(self, state):
        if state==[1,2,3,4,5,6,7,8,0]:
            return True
        else:
            return False

    def draw(self,s):
        for x in range(3):
            print(str(s[x])+ "  ",end="")
        print()
        for x in range(3):
            print(str(s[x+3])+ "  ",end="")
        print()
        for x in range(3):
            print(str(s[x+6])+ "  ",end="")
        print()


    def swap(self,a,b,c):
        if c == 'R':
            x = a.state[:]
            x[b] = x[b+1]
            x[b+1]= 0
            return x
        if c == 'L':
            x = a.state[:]
            x[b] = x[b-1]
            x[b-1]= 0
            return x
        if c == 'D':
            x = a.state[:]
            x[b] = x[b+3]
            x[b+3]= 0
            return x
        if c == 'U':
            x = a.state[:]
            x[b] = x[b-3]
            x[b-3]= 0
            return x
        
    def createChild(self, n):
        childlist=[]
        for i in range(9):
            if n.state[i]==0:
                if i==6 or i==7 or i==8:
                    newstate = self.swap(n,i,'U')
                    newnode=Node(newstate, 'U', n, n.cost+1)
                    childlist.append(newnode)

                if i==1 or i==4 or i==7:
                    newstate = self.swap(n,i,'L')
                    newnode=Node(newstate, 'L', n, n.cost+1)
                    childlist.append(newnode)
                    newstate = self.swap(n,i,'R')
                    newnode=Node(newstate, 'R', n, n.cost+1)
                    childlist.append(newnode)
                if i==3 or i==4 or i==5:
                    newstate = self.swap(n,i,'U')
                    newnode=Node(newstate, 'U', n, n.cost+1)
                    childlist.append(newnode)
                    newstate = self.swap(n,i,'D')
                    newnode=Node(newstate, 'D', n, n.cost+1)
                    childlist.append(newnode)
                if i==0 or i==3 or i==6:
                    newstate = self.swap(n,i,'R')
                    newnode=Node(newstate, 'R', n, n.cost+1)
                    childlist.append(newnode)
                if i==0 or i==1 or i==2:
                    newstate = self.swap(n,i,'D')
                    newnode=Node(newstate, 'D', n, n.cost+1)
                    childlist.append(newnode)
                if i==2 or i==5 or i==8:
                    newstate = self.swap(n,i,'L')
                    newnode=Node(newstate, 'L', n, n.cost+1)
                    childlist.append(newnode)
                
                return childlist

    def clear(self):
        self.count =0
        self.fringelen=0
        self.fringemax=1
        self.depthmax=0
        
    def DFS(self):
        self.clear()
        closed=[]
        fringe=[]
        n=Node(self.initial_state)
        fringe.append(n)
        while fringe:
            n=fringe.pop()
            if self.GoalTest(n.state):
                self.fringelen = len(fringe)
                return n
            if n.state not in closed:
                closed.append(n.state)
                for i in self.createChild(n):
                    fringe.append(i)
                    self.count=self.count+1
                    if i.cost>self.depthmax:
                        self.depthmax=i.cost 
                if len(fringe)>self.fringemax:
                        self.fringemax=len(fringe)

    def BFS(self, istate):
        self.clear()
        closed=[]
        fringe=deque()
        n=Node(istate)
        fringe.append(n)
        count =0
        while fringe:
            n=fringe.popleft()
            if self.GoalTest(n.state):
                self.fringelen = len(fringe)
                return n
            if n.state not in closed:
                closed.append(n.state)
                for i in self.createChild(n):
                    fringe.append(i)
                    self.count=self.count+1
                    if i.cost>self.depthmax:
                        self.depthmax=i.cost         
                if len(fringe)>self.fringemax:
                        self.fringemax=len(fringe)

    def A(self):
        self.clear()
        closed=[]
        fringe= []
        n=Node(self.initial_state)
        heapq.heappush(fringe,(n.menhaten(),n))
        while fringe:
            n=heapq.heappop(fringe)
            if self.GoalTest(n[1].state):
                self.fringelen = len(fringe)         #تخزين حجم الفرينج لما لقا الحل 
                return n[1]
            if n[1].state not in closed:
                closed.append(n[1].state)
                for i in self.createChild(n[1]):
                    heapq.heappush(fringe,(i.menhaten(),i))
                    self.count=self.count+1          #حساب عدد النودات اللي صار إلهم تفريع
                    if i.cost>self.depthmax:
                        self.depthmax=i.cost         #اعمق لفل وصل إله خلال البحث
                if len(fringe)>self.fringemax:
                        self.fringemax=len(fringe)   #تخزين اكبر حجم وصل له الفرينج بمقارنته بالحجم الحالي وتخزين الجديد اذا اكب
                        
flag =True
while flag:
    count =0
    path=[]
    i = input("Enter the start state:")
    j = int(input("1-DFS 2-BFS 3-A*:"))
    print()
    i= [int(j) for j in i.replace(" ","")]
    i=[i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8]]
    v=EightPuzzle(i)
    if j==1:
        start =time.time()
        n=v.DFS()
        end=time.time()
        print("DFS")
    elif j==2:
        start =time.time()
        n=v.BFS(i)
        end=time.time()
        print("BFS")
    elif j==3:
        start =time.time()
        n=v.A()
        end=time.time()
        print("A*")

    while not(n.state==i):
        path.append(n)
        count=count+1            #كونتر لعدد الخطوات للوصول للحل
        n=n.parent
    path.append(n)
    path.reverse()

    print("path to Goal: ")
    print("Initial state: ")
    for j in path:
        print("******************")
        if j.state==[1,2,3,4,5,6,7,8,0]:
            print("Goal state: ")
        v.draw(j.state)        #رسم الستيت
        print()
        print("Action: "+ str(j.action))
        print("Cost: "+ str(j.cost))
        #print(n.menhaten())    #طبعة قيمة المنهاتن للستيت

    print()
    print()
    print("Cost of path : " + str(count))
    print("nodes expanded: "+ str(v.count))
    print("fringe size: "+ str(v.fringelen))
    print("max fringe size: "+ str(v.fringemax))
    print("search depth: "+ str(count))
    print("max search depth: "+ str(v.depthmax))
    print("Running time: "+str(end-start))

    flag=(input("again?(y-n): ")is"y")
    

        
    
