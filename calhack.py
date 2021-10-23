from random import randint
class lister:
    def __init__(self):
        self.x=0
    def __str__(self):
        return f"[[1,2,3]\n[2,3,4]\n[3,4,5]]"
y=lister()
print(y)

def mergable(lst,direction):
    if direction==-1:
        lst.reverse()
    for x in range(0,len(lst)-1):
        if lst[x]==lst[x+1] and lst[x]!=0:
            return True
        if x>0:
            if (lst[x]==0 and lst[x-1]!=0) or (lst[x]!=0 and lst[x+1]==0):
                return True
    return False

    
class gamestate:
    grid=[]
    def __init__(self):
        self.score=0
        self.record=2
        self.old=[]
    def start_game(self,grid):
        for x in range(grid.scale):
            for y in range(grid.scale):
                grid.layout[x][y]=0
        grid.spawn_random()
        grid.spawn_random()
        self.grid=grid
        print(grid)
    def go_back(self,grid):
        if self.old!=[]:
            grid.layout=self.old
        print(grid)
    def victory(self):
        print(f"You've won(kinda), Yeah! Type g.start_game(grid1) to restart a new game or continue playing until you reach the ultimate goal of {2**((self.grid.scale**2)+1)} ")
    def game_over(self):
        print(f"Game over, your record is {self.record} and your score is {self.score}! Type g.start_game(grid1) to restart a new game or g.go_back(grid1) to fix your mistake!")

class grid:
    def __init__(self,n=4):
       self.layout=[]
       self.scale=n
       for x in range(n):
           j=[]
           for y in range(n):
               j.append(0)
           self.layout.append(j)
    def __str__(self):
        for x in range(self.scale):
            print(self.row(x))
        
    def row(self,n):
        lst=self.layout[n][:]
        return lst
    def column(self,n):
        lst=[]
        for x in range(self.scale):
            lst.append(self.layout[x][n])
        return lst
    def spawn_random(self):
        null_space=[]
        for x in range(self.scale):
            for y in range(self.scale):
                if self.layout[x][y]==0:
                    null_space.append([x,y])
        t=randint(0,len(null_space)-1)
        j=randint(0,3)
        if j==3:
            self.layout[null_space[t][0]][null_space[t][1]]=4
        else:
            self.layout[null_space[t][0]][null_space[t][1]]=2

    def upable(self):
        for x in range(self.scale):
            if mergable(self.column(x),-1):
                return True
        return False
    def downable(self):
        for x in range(self.scale):
            if mergable(self.column(x),1):
                return True
        return False
    def leftable(self):
        for x in range(self.scale):
            if mergable(self.row(x),-1):
                return True
        return False
    def rightable(self):
        for x in range(self.scale):
            if mergable(self.row(x),1):
                return True
        return False
    def up(self,gamestate):
        if self.upable():
            gamestate.old=[]
            for x in range(self.scale):
                gamestate.old.append(self.row(x))
            for x in range(self.scale):
                lster=self.column(x)
                y=0
                while y < len(lster):
                    if lster[y]==0:
                        lster.pop(y)
                    else:
                        y+=1
                j=0
                while j<len(lster)-1:
                    if lster[j]==lster[j+1]:
                        lster[j]*=2
                        gamestate.score+=lster[j]
                        if lster[j]>gamestate.record:
                            gamestate.record=lster[j]
                        lster.pop(j+1)
                    j=j+1
                for u in range(self.scale):
                    self.layout[u][x]=0
                for t in range(len(lster)):
                    self.layout[t][x]=lster[t]
            self.spawn_random()
            if not (self.upable() or self.rightable() or self.downable() or self.leftable()):
                gamestate.game_over()
            elif gamestate.record==2048:
                gamestate.victory()
            else:
                print(self)
        else:
            print("Invalid operation")
    def down(self,gamestate):
        if self.downable():
            gamestate.old=[]
            for x in range(self.scale):
                gamestate.old.append(self.row(x))
            for x in range(self.scale):
                lster=self.column(x)
                y=0
                while y < len(lster):
                    if lster[y]==0:
                        lster.pop(y)
                    else:
                        y+=1
                lster.reverse()
                j=0
                while j<len(lster)-1:
                    if lster[j]==lster[j+1]:
                        lster[j]*=2
                        gamestate.score+=lster[j]
                        if lster[j]>gamestate.record:
                            gamestate.record=lster[j]
                        lster.pop(j+1)
                    j=j+1
            
                for u in range(self.scale):
                    self.layout[u][x]=0
                for t in range(len(lster)):
                    self.layout[self.scale-t-1][x]=lster[t]
            self.spawn_random()
            if not (self.upable() or self.rightable() or self.downable() or self.leftable()):
                gamestate.game_over()
            elif gamestate.record==2048:
                gamestate.victory()
            else:
                print(self)
        else:
            print("Invalid operation")
    def left(self,gamestate):
        if self.leftable():
            gamestate.old=[]
            for x in range(self.scale):
                gamestate.old.append(self.row(x))
            for x in range(self.scale):
                lster=self.row(x)
                y=0
                while y < len(lster):
                    if lster[y]==0:
                        lster.pop(y)
                    else:
                        y+=1
                j=0
                while j<len(lster)-1:
                    if lster[j]==lster[j+1]:
                        lster[j]*=2
                        gamestate.score+=lster[j]
                        if lster[j]>gamestate.record:
                            gamestate.record=lster[j]
                        lster.pop(j+1)
                    j=j+1
                for u in range(self.scale):
                    self.layout[x][u]=0
                for t in range(len(lster)):
                    self.layout[x][t]=lster[t]
            self.spawn_random()
            if not (self.upable() or self.rightable() or self.downable() or self.leftable()):
                gamestate.game_over()
            elif gamestate.record==2048:
                gamestate.victory()
            else:
                print(self)
        else:
            print("Invalid operation")
    def right(self,gamestate):
        if self.rightable():
            gamestate.old=[]
            for x in range(self.scale):
                gamestate.old.append(self.row(x))
            for x in range(self.scale):
                lster=self.row(x)
                y=0
                while y < len(lster):
                    if lster[y]==0:
                        lster.pop(y)
                    else:
                        y+=1
           
                lster.reverse()
                j=0
                while j<len(lster)-1:
                    if lster[j]==lster[j+1]:
                        lster[j]*=2
                        gamestate.score+=lster[j]
                        if lster[j]>gamestate.record:
                            gamestate.record=lster[j]
                        lster.pop(j+1)
                    j=j+1
                lster.reverse()
                for u in range(self.scale):
                    self.layout[x][u]=0
                for t in range(len(lster)):
                    self.layout[x][self.scale-len(lster)+t]=lster[t]
            self.spawn_random()
            if not (self.upable() or self.rightable() or self.downable() or self.leftable()):
                gamestate.game_over()
            elif gamestate.record==2048:
                gamestate.victory()
            else:
                print(self)
        else:
            print("Invalid operation")




g=gamestate()
grid1=grid()
g.start_game(grid1)






                    
    
    
