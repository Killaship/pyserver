import socket

host = "127.0.0.1" # TODO, move this to config file
port = 80

def TCPstart():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5) # normal max is 5 users queued
    print("Listening on ", sock.getsockname())
    while True:
        user, addr = sock.accept()
        print(user, " connected")
        data = user.recv(4096) # read first 4K of data
        user.sendall(handler(data))
        
        user.close()


def handler(data):   
    response = b"HTTP/1.1 200 OK\r\n"
    bline = b"\r\n"
    body = b"test, hello!"
    return b"".join([response, bline, body])
    
TCPstart()
