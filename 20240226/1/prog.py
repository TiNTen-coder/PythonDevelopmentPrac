import cowsay


class Field:
    matrix = [[None for i in range(10)] for j in range(10)]


class Player:
    x = 0
    y = 0

    def move(self, flag):
        match flag:
            case "up":
                self.y = (self.y - 1) % 10
            case "down":
                self.y = (self.y + 1) % 10
            case "left":
                self.x = (self.x - 1) % 10
            case "right":
                self.x = (self.x + 1) % 10
        print(f'Moved to ({self.x}, {self.y})')
        self.encounter(self.x, self.y)

    def encounter(self, x, y):
        if Field.matrix[x][y] is not None:
            print(cowsay.cowsay(Field.matrix[x][y].phrase))


class Monster:
    x = None
    y = None
    phrase = None

    def addmonster(self, x, y, hello):
        match Field.matrix[x][y]:
            case None:
                self.x = x
                self.y = y
                self.phrase = hello
                print(f'Added monster to ({x}, {y}) saying {hello}')
            case _:
                self.phrase = hello
                print('Replaced the old monster')


field = Field()
player = Player()
while True:
    try:
        com = input().split()
    except Exception:
        return
    match com[0]:
        case "up" | "down" | "left" | "right":
            if len(com) != 1:
                print('Invalid arguments')
            else:
                player.move(com[0])
        case "addmon":
            if len(com) != 4:
                print('Invalid arguments')
            else:
                x = com[1]
                y = com[2]
                phrase = com[3]
                if x.isdigit() and y.isdigit() and 0 <= int(x) <= 9 and 0 <= int(y) <= 9:
                    x = int(x)
                    y = int(y)
                    tmp = Monster()
                    tmp.addmonster(x, y, phrase)
                    field.matrix[x][y] = tmp
                else:
                    print('Invalid arguments')
        case _:
            print('Invalid commands')
