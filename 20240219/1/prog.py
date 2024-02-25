import sys
import os
import zlib
import glob


if len(sys.argv) == 1:
    print("Requires at least 1 argument.")
elif len(sys.argv) == 2:
    for i in glob.iglob():
        for j in os.scandir(i):
            print(j.name)
else:
    last_commit = open(sys.argv[1] + '/.git/refs/heads/' + sys.argv[2], "r").read()[:-1]
    with open(sys.argv[1] + '/.git/objects/' + last_commit[0:2] + '/' + last_commit[2:], "rb") as f:
        data = zlib.decompress(f.read()).partition(b'\x00')[2].split(b'\n')
        print(data[0].decode())
        print(data[1].decode())
        print(*data[2].decode().split(' ')[:-2])
        print(*data[3].decode().split(' ')[:-2])
        print('\n', data[-2].decode(), '\n\n', sep='')
    while data:
        print(f'TREE for commit {last_commit}')
        tree_id = data[0].decode().split(' ')[1]
        with open(sys.argv[1] + '/.git/objects/' + tree_id[0:2] + '/' + tree_id[2:], 'rb') as tree:
            data = zlib.decompress(tree.read()).partition(b'\x00')[2]
        while data:
            name = data.partition(b'\00')[0].split(b' ')[-1].decode()
            id = data.partition(b'\00')[2][:20].hex()
            try:
                with open(sys.argv[1] + '/.git/objects/' + id[0:2] + '/' + id[2:], 'rb') as item:
                    it_type = zlib.decompress(item.read()).partition(b' ')[0].decode()
            except Exception:
                print(f'blob {id}\t{name}')
                break
            data = data.partition(b'\00')[2][20:]
            print('---' * (it_type != 'tree') + f'{it_type} {id}\t{name}')
        if not data[3]:
            break
        last_commit = data[1].decode().split(' ')[1]
        try:
            with open(sys.argv[1] + '/.git/objects/' + last_commit[0:2] + '/' + last_commit[2:], 'rb') as commit:
                data = zlib.decompress(commit.read()).partition(b'\00')[2].split(b'\n')
        except Exception:
            break
