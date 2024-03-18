import sys
import socket
import shlex

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while data := conn.recv(1024):
            com = shlex.split(data.decode())
            if len(com) > 1 and com[0] == 'print':
                conn.sendall(shlex.join(com[1:]).encode())
            if len(com) > 1 and com[0] =='info':
                address, port = s.get_extra_info('peername')
                if com[1] == 'port':
                    conn.sendall(port.encode())
                else:
                    conn.sendall(address.encode())
            #print(s.recv(1024).rstrip().decode())
