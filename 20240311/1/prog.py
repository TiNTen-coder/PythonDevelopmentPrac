import cowsay
import io
import shlex
import sys
import cmd

class CommandLine(cmd.Cmd):
    prompt = '>>> '
    intro = "<<< Welcome to Python-MUD 0.1.2 >>>"
    
    def do_default(self):
        print("Invalid arguments")
    
    def do_EOF(self, args):
        return True

    def do_up(self, com):
        if com:
            print('Alert: Move commands dont support the positional arguments')
        player.move('up')

    def do_down(self, com):
        if com:
            print('Alert: Move commands dont support the positional arguments')
        player.move('down')

    def do_left(self, com):
        if com:
            print('Alert: Move commands dont support the positional arguments')
        player.move('left')

    def do_right(self, com):
        if com:
            print('Alert: Move commands dont support the positional arguments')
        player.move('right')

    def do_addmon(self, com):
        try:
            com = shlex.split(com)
        except ValueError:
            print('Invalid arguments')
            return True
        except Exception:
            return True
        print(com)
        if len(com) != 8 or 'coords' not in com or 'hello' not in com or 'hp' not in com:
            print('Invalid arguments')
        else:
            name = com[0]
            x = com[com.index('coords') + 1]
            y = com[com.index('coords') + 2]
            phrase = com[com.index('hello') + 1]
            hp = com[com.index('hp') + 1]
            if x.isdigit() and y.isdigit() and 0 <= int(x) <= 9 and 0 <= int(y) <= 9 and hp.isdigit():
                x = int(x)
                y = int(y)
                hp = int(hp)
                try:
                    tmp = Monster()
                    tmp.addmonster(name, x, y, phrase, hp)
                    field.matrix[x][y] = tmp
                except NameError: 
                    pass
            else:
                print('Invalid arguments')
        print(Field.matrix)

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
            if Field.matrix[x][y].name == 'jgsbat':
                custom_monster = cowsay.read_dot_cow(io.StringIO("""
                $the_cow = <<EOC;
                         $thoughts
                          $thoughts
                    ,_                    _,
                    ) '-._  ,_    _,  _.-' (
                    )  _.-'.|\\--//|.'-._  (
                     )'   .'\/o\/o\/'.   `(
                      ) .' . \====/ . '. (
                       )  / <<    >> \  (
                        '-._/``  ``\_.-'
                  jgs     __\\'--'//__
                         (((""`  `"")))
                EOC
                """))
                print(cowsay.cowsay(Field.matrix[x][y].phrase, cowfile=custom_monster))
            else:
                print(cowsay.cowsay(Field.matrix[x][y].phrase, cow=Field.matrix[x][y].name))



class Monster:
    name = None
    x = None
    y = None
    phrase = None
    hitpoints = None

    def addmonster(self, name, x, y, hello, hitpoints):
        match Field.matrix[x][y]:
            case None:
                if name in cowsay.list_cows() or name == 'jgsbat':
                    self.name = name
                    self.x = x
                    self.y = y
                    self.phrase = hello
                    self.hitpoints = hitpoints
                    print(f'Added monster to ({x}, {y}) saying {hello}')
                else:
                    print('Cannot add unknown monster')
                    raise NameError
            case _:
                self.phrase = hello
                self.hitpoints = hitpoints
                print('Replaced the old monster')

if __name__ == '__main__':
    field = Field()
    player = Player()
    CommandLine().cmdloop()
   
