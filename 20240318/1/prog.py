import cowsay
import io
import shlex
import sys
#import cmd
import readline
import rlcompleter
import asyncio

WEAPON_TOOLS = {
    'sword': 10,
    'spear': 15,
    'axe': 20
}
clients = {}
MONSTERS = set(cowsay.list_cows()) | set(['jgsbat'])

async def parse_the_command(data, me):
    if data:
        com = data[0]
        match com:
            case 'up':
                if com:
                    await clients[me].put('Alert: Move commands dont support the positional arguments')
                await player.move('up', me)
            case 'down':
                if com:
                    await clients[me].put('Alert: Move commands dont support the positional arguments')
                await player.move('down', me)
            case 'left':
                if com:
                    await clients[me].put('Alert: Move commands dont support the positional arguments')
                await player.move('left', me)
            case 'right':       
                if com:
                    await clients[me].put('Alert: Move commands dont support the positional arguments')
                await player.move('right', me)
            case 'attack':
                try:
                    args = shlex.split(data[1])
                    print(args)
                except ValueError:
                    await clients[me].put('Invalid arguments')
                    return True
                except Exception as E:
                    print(E)
                    return True
                if len(args) == 3 and 'with' in args:
                    await player.attack(args[0], args[2], me)
                elif len(args) == 1 and args[0] in MONSTERS:
                    await player.attack(args[0], 'sword', me)
                else:
                    await clients[me].put('Invalid arguments')
            case 'addmon':   
                try:
                    com = shlex.split(data[1])
                except ValueError:
                    await clients[me].put('Invalid arguments')
                    return True
                except Exception:
                    return True
                if len(com) != 8 or 'coords' not in com or 'hello' not in com or 'hp' not in com:
                    await clients[me].put('Invalid arguments')
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
                            await tmp.addmonster(name, x, y, phrase, hp, me)
                            field.matrix[x][y] = tmp
                        except NameError: 
                            pass
                    else:
                        await clietns[me].put('Invalid arguments')
            case _:
                await clients[me].put('Invalid arguments')


class Field:
    matrix = [[None for i in range(10)] for j in range(10)]


class Player:
    x = 0
    y = 0
    
    async def move(self, flag, me):
        match flag:
            case "up":
                self.y = (self.y - 1) % 10
            case "down":
                self.y = (self.y + 1) % 10
            case "left":
                self.x = (self.x - 1) % 10
            case "right":
                self.x = (self.x + 1) % 10
        await clients[me].put(f'Moved to ({self.x}, {self.y})')
        await self.encounter(self.x, self.y, me)

    async def encounter(self, x, y, me):
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
                await clients[me].put(cowsay.cowsay(Field.matrix[x][y].phrase, cowfile=custom_monster))
            else:
                await clients[me].put(cowsay.cowsay(Field.matrix[x][y].phrase, cow=Field.matrix[x][y].name))

    async def attack(self, monster_name, weapon_name, me):
        if weapon_name not in WEAPON_TOOLS.keys():
            await clients[me].put('Unknown weapon')
            return
        if Field.matrix[self.x][self.y].name != monster_name:
            await clients[me].put(f'No {monster_name} here')
        else:
            await clients[me].put(f'Attacked {Field.matrix[self.x][self.y].name}, damage {min(WEAPON_TOOLS[weapon_name], Field.matrix[self.x][self.y].hitpoints)} hp')
            Field.matrix[self.x][self.y].hitpoints = max(Field.matrix[self.x][self.y].hitpoints - WEAPON_TOOLS[weapon_name], 0)
            if not Field.matrix[self.x][self.y].hitpoints:
                await clients[me].put(f'{Field.matrix[self.x][self.y].name} died')
                Field.matrix[self.x][self.y] = None
            else:
                await clients[me].put(f'{Field.matrix[self.x][self.y].name} now has {Field.matrix[self.x][self.y].hitpoints}')

class Monster:
    name = None
    x = None
    y = None
    phrase = None
    hitpoints = None

    async def addmonster(self, name, x, y, hello, hitpoints, me):
        match Field.matrix[x][y]:
            case None:
                if name in MONSTERS:
                    self.name = name
                    self.x = x
                    self.y = y
                    self.phrase = hello
                    self.hitpoints = hitpoints
                    await clients[me].put(f'Added monster to ({x}, {y}) saying {hello}')
                else:
                    await clients[me].put('Cannot add unknown monster')
                    raise NameError
            case _:
                self.phrase = hello
                self.hitpoints = hitpoints
                await clients[me].put('Replaced the old monster')

async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                data = q.result().decode().strip().split(maxsplit=1)
                answer = await parse_the_command(data, me)
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
        if answer:
            break
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    field = Field()
    player = Player()
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    #CommandLine().cmdloop()
    asyncio.run(main())
