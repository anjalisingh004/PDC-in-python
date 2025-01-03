import socket, select, sys
TCP_IP = '172.24.96.81'
TCP_PORT = 4715

BUFFER_SIZE = 1024
MESSAGE = "nh ge hy"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, 4715))
s.send(MESSAGE)
socket_list = [sys.stdin, s]

while 1:
    read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])


    for sock in read_sockets:
        # incoming message from remote server
        if sock == s:
            data = sock.recv(4096)
            if not data:
                print('\nDisconnected from server')
                sys.exit()
            else:
                sys.stdout.write("\n")
                message = data.decode()
                sys.stdout.write(message)
                sys.stdout.write('<Me> ')
                sys.stdout.flush()

        else:
            msg = sys.stdin.readline()
            s.send(bytes(msg))
            sys.stdout.write('<Me> ')
            sys.stdout.flush()
