from random import randint

def mergable(original, direction):
    lst = original[:]
    if direction==-1:
        lst.reverse()
    for x in range(0, len(lst)-1):
        if (lst[x] == lst[x+1] and lst[x]!=0) or (lst[x] != 0 and lst[x+1] == 0):
            return True
    return False

    
class gamestate:
    def __init__(self, grid, undo_limit=10):
        self.score = 0
        self.record = 0
        self.history = []
        self.grid = grid
        self.undo_limit = undo_limit

    def start_game(self):
        self.grid.start()
        print(self.grid)

    def undo(self):
        if self.history:
            grid, self.score, self.record = self.history.pop()
            self.grid.change_grid(grid)
            print(self.grid)
        else:
            print("Can not undo further")
        
    
    def move(self, dir):
        res = 0
        record = 0
        prev = self.grid.get_grid()
        copy = [prev[i][:] for i in range(len(prev))]
        self.history.append((copy, self.score, self.record))
        if dir == "right":
            res, record = self.grid.right()
        elif dir == "left":
            res, record = self.grid.left()
        elif dir == "down":
            res, record = self.grid.down()
        elif dir == "up":
            res, record = self.grid.up()
        else:
            print("invalid move")
        if res != None:
            print(self.grid)
            self.score += res
            self.record = max(self.record, record)
            if len(self.history) > self.undo_limit:
                self.history.pop(0)
            if self.grid.stuck():
                self.game_over()
            if self.record == 2048:
                self.victory()
        else:
            self.history.pop()
            
    def victory(self):
        print(f"You've won(kinda), Yeah! Type g.start_game() to restart a new game or continue playing to get bigger tiles")

    def game_over(self):
        print(f"Game over, your record is {self.record} and your score is {self.score}! Type g.start_game() to restart a new game or g.undo() to fix your mistake!")

class grid:
    def __init__(self, n=4):
       self.layout=[[0 for i in range(n)] for j in range(n)]
       self.scale=n
       
    def __str__(self):
        res = ""
        for x in range(self.scale):
            res += str(self.layout[x])
            res += "\n"
        return res
    
    def start(self):
        for i in range(self.scale):
            for j in range(self.scale):
                self.layout[i][j] = 0
        self.spawn_random()
        self.spawn_random()
    
    def get_grid(self):
        return self.layout
    
    def change_grid(self, grid):
        self.layout = grid
        
    def row(self, n):
        return self.layout[n]
        
    def column(self, n):
        lst = []
        for x in range(self.scale):
            lst.append(self.layout[x][n])
        return lst
    
    def spawn_random(self):
        null_space = []
        for x in range(self.scale):
            for y in range(self.scale):
                if self.layout[x][y] == 0:
                    null_space.append([x, y])
        if not null_space:
            print("can't spawn")
            return
        t = randint(0, len(null_space) - 1)
        j = randint(0, 9)
        if j == 9:
            self.layout[null_space[t][0]][null_space[t][1]] = 4
        else:
            self.layout[null_space[t][0]][null_space[t][1]] = 2

    def stuck(self):
        return not (self.upable() or self.downable() or self.leftable() or self.rightable())

    def upable(self):
        for x in range(self.scale):
            if mergable(self.column(x), -1):
                return True
        return False
    
    def downable(self):
        for x in range(self.scale):
            if mergable(self.column(x), 1):
                return True
        return False
    
    def leftable(self):
        for x in range(self.scale):
            if mergable(self.row(x), -1):
                return True
        return False
    
    def rightable(self):
        for x in range(self.scale):
            if mergable(self.row(x), 1):
                return True
        return False
    
    def up(self):
        if self.upable():
            score = 0
            record = 0
            for x in range(self.scale):
                col = self.column(x)
                new_col = []
                if col[0]:
                    new_col.append(col[0])
                i = 1
                while i < len(col):
                    if col[i]:
                        if new_col and new_col[-1] == col[i]:
                            new_col[-1] = 2 * new_col[-1]
                            score += new_col[-1]
                            record = max(record, new_col[-1])
                        else:
                            new_col.append(col[i])
                    i += 1
                for i in range(len(col)):
                    if i < len(new_col):
                        self.layout[i][x] = new_col[i]
                    else:
                        self.layout[i][x] = 0
            self.spawn_random()
            return (score, record)
        else:
            print("Can not move up")
            return (None, None)

    def down(self):
        if self.downable():
            score = 0
            record = 0
            for x in range(self.scale):
                col = self.column(x)
                new_col = []
                if col[-1]:
                    new_col.append(col[-1])
                i = len(col) - 2
                while i >= 0:
                    if col[i]:
                        if new_col and new_col[0] == col[i]:
                            new_col[0] = 2 * new_col[0]
                            score += new_col[0]
                            record = max(record, new_col[0])
                        else:
                            new_col.insert(0, col[i])
                    i -= 1
                for i in range(len(col) - len(new_col), len(col)):
                    self.layout[i][x] = new_col[i - (len(col) - len(new_col))]
                for i in range(len(col) - len(new_col)):
                    self.layout[i][x] = 0
            self.spawn_random()
            return (score, record)
        else:
            print("Can not move down")
            return (None, None)

    def left(self):
        if self.leftable():
            score = 0
            record = 0
            for x in range(self.scale):
                row = self.row(x)
                new_row = []
                if row[0]:
                    new_row.append(row[0])
                i = 1
                while i < len(row):
                    if row[i]:
                        if new_row and new_row[-1] == row[i]:
                            new_row[-1] = 2 * new_row[-1]
                            score += new_row[-1]
                            record = max(record, new_row[-1])
                        else:
                            new_row.append(row[i])
                    i += 1
                for i in range(len(row)):
                    if i < len(new_row):
                        self.layout[x][i] = new_row[i]
                    else:
                        self.layout[x][i] = 0
            self.spawn_random()
            return (score, record)
        else:
            print("Can not move left")
            return (None, None)

    def right(self):
        if self.rightable():
            for x in range(self.scale):
                score = 0
                record = 0
                row = self.row(x)
                new_row = []
                if row[-1]:
                    new_row.append(row[-1])
                i = len(row) - 2
                while i >= 0:
                    if row[i]:
                        if new_row and new_row[0] == row[i]:
                            new_row[0] = 2 * new_row[0]
                            score += new_row[0]
                            record = max(record, new_row[0])
                        else:
                            new_row.insert(0, row[i])
                    i -= 1
                for i in range(len(row) - len(new_row), len(row)):
                    self.layout[x][i] = new_row[i - (len(row) - len(new_row))]
                for i in range(len(row) - len(new_row)):
                    self.layout[x][i] = 0
            self.spawn_random()
            return (score, record)
        else:
            print("Can not move right")
            return (None, None)



g = grid()
game = gamestate(g)
game.start_game()

print("Enter action (up/down/left/right/undo or quit)")
while True:
    cmd = input(">").strip().lower()
    if cmd == "quit":
        break
    if cmd in ("up", "down", "left", "right"):
        game.move(cmd)
        print(game.score)
        print(game.record)
    elif cmd == "undo":
        game.undo()
    else:
        print("Invalid move. Try: up, down, left, right, or undo")






                    
    
    
