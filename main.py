import socket


try:
    with open('pyserver.conf', 'r') as f:
        conf = f.readlines()
        host = conf[0].strip()
        port = int(conf[1].strip())
        version =  str(conf[2].strip())
    f.close()
    print("Read config file successfully!")
    
except Exception as e:
    print("Error reading pyserver.conf!\n\n", e)
    raise SystemExit(1)

def TCPstart():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # so it doesn't hog that port for another minute after the program ends
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
    header = b"".join([
        bytes(str("Server: pyserver"+version+"\r\n"), 'utf-8'),
        b"Content-Type: text/html\r\n"
    ])
    bline = b"\r\n"
    body = b"test, hello!"
    return b"".join([response, header, bline, body])

    
TCPstart()
