import socket
import time
import sys
current_module = sys.modules[__name__]

try:
    with open('pyserver.conf', 'r') as f:
        conf = f.readlines()
        host = conf[0].strip()
        port = int(conf[1].strip())
        version = str(conf[2].strip())
        sourcefile = str(conf[3].strip())
        verbosity = int(conf[4].strip())
    f.close()
    print("Read config file successfully!")
    
except Exception as e:
    print("Error reading pyserver.conf!\n\n", e)
    raise SystemExit(1)

try:
    with open(sourcefile, 'r') as f:
        source = f.read()
    f.close()
    print("Read server content successfully!")
    
except Exception as e:
    print("Error reading server content!\n\n", e)
    raise SystemExit(1)    
    
    
def TCPstart():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # so it doesn't hog that port for another minute after the program ends
    sock.bind((host, port))
    sock.listen(5) # normal max is 5 users queued
    print("Listening on ", sock.getsockname())
    while True:
        user, addr = sock.accept()
        print(user, " connected, time=", time.time())
        data = user.recv(4096) # read first 4K of data
        user.sendall(handler(data))
        
        user.close()
class Request:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = "1.1"
        self.parse(data)
    
    def parse(self, data):
        lines = data.split(b"\r\n")
        request = lines[0]
        chunks = request.split(b" ")
        self.method = chunks[0].decode()
        if(len(chunks) > 1):
            self.uri = chunks[1].decode()
        if(len(chunks) > 2):
            self.httpver = chunks[2].decode()
def handler_GET(data):
    response = b"HTTP/1.1 200 OK\r\n"
    header = b"".join([
        bytes(str("Server: pyserver"+version+"\r\n"), 'utf-8'),
        b"Content-Type: text/html\r\n"
    ])
    bline = b"\r\n"
    body = bytes(source, "utf-8")
    return b"".join([response, header, bline, body])

def handler_501(data): # TODO: move error pages to separate folder
    response = b"HTTP/1.1 501 Not Implemented\r\n"
    header = b"".join([
        bytes(str("Server: pyserver"+version+"\r\n"), 'utf-8'),
        b"Content-Type: text/html\r\n"
    ])
    bline = b"\r\n"
    body = b"<b><h1>HTTP 501: Not Implemented</b></h1><br><br><p>(C) 2023 Killaship, pyserver project<br><a href='https://github.com/Killaship/pyserver'>github link</a></p>"
    return b"".join([response, header, bline, body])


def handler(data):   
    request = Request(data)
    print("new request:\n"+str(data))
    try:
        methodhandler = getattr(current_module, 'handler_%s' % request.method) # useful hack I found
    except AttributeError:
        methodhandler = handler_501
    response = methodhandler(request)
    print("response:\n"+str(response)+"\n")
    return response
    
TCPstart()
