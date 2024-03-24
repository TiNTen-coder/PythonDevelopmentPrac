import cowsay
import io
import shlex
import sys
import cmd
import readline
import rlcompleter

WEAPON_TOOLS = {
    'sword': 10,
    'spear': 15,
    'axe': 20
}

MONSTERS = set(cowsay.list_cows()) | set(['jgsbat'])

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
    
    def do_attack(self, args):
        try:
            args = shlex.split(args)
        except ValueError:
            print('Invalid arguments')
            return True
        except Exception:
            return True
        if len(args) == 3 and 'with' in args:
            player.attack(args[0], args[2])
        elif len(args) == 1 and args[0] in MONSTERS:
            player.attack(args[0], 'sword')
        else:
            print('Invalid arguments')
    
    def complete_attack(self, text, line, begidx, endidx):
        args = shlex.split(line[:begidx], False, False)
        if args[-1] == 'with':
            return [c for c in WEAPON_TOOLS if c.startswith(text)]
        elif args[-1] == 'attack':
            return [c for c in MONSTERS if c.startswith(text)]
    
    def do_addmon(self, com):
        try:
            com = shlex.split(com)
        except ValueError:
            print('Invalid arguments')
            return True
        except Exception:
            return True
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
    
    def complete_addmon(self, text, line, begidx, endidx):
        args = shlex.split(line[:begidx])
        if args[-1] == 'addmon':
            return [c for c in MONSTERS if c.startswith(text)]
        elif args[-1] in MONSTERS:
            return [c for c in ['coords', 'hello', 'hp'] if c.startswith(text)]
        elif args[-1] == 'coords':
            return [c for c in map(lambda x: str(x), range(10)) if c.startswith(text)]

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

    def attack(self, monster_name, weapon_name):
        if weapon_name not in WEAPON_TOOLS.keys():
            print('Unknown weapon')
            return
        if Field.matrix[self.x][self.y].name != monster_name:
            print(f'No {monster_name} here')
        else:
            print(f'Attacked {Field.matrix[self.x][self.y].name}, damage {min(WEAPON_TOOLS[weapon_name], Field.matrix[self.x][self.y].hitpoints)} hp')
            Field.matrix[self.x][self.y].hitpoints = max(Field.matrix[self.x][self.y].hitpoints - WEAPON_TOOLS[weapon_name], 0)
            if not Field.matrix[self.x][self.y].hitpoints:
                print(f'{Field.matrix[self.x][self.y].name} died')
                Field.matrix[self.x][self.y] = None
            else:
                print(f'{Field.matrix[self.x][self.y].name} now has {Field.matrix[self.x][self.y].hitpoints}')

class Monster:
    name = None
    x = None
    y = None
    phrase = None
    hitpoints = None

    def addmonster(self, name, x, y, hello, hitpoints):
        match Field.matrix[x][y]:
            case None:
                if name in MONSTERS:
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
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    CommandLine().cmdloop()
   
