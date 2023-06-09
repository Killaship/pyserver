import socket
import time
import sys
import os
import mimetypes

file_size = 0

implementedmethods = "Allow: OPTIONS, GET, HEAD\r\n"
current_module = sys.modules[__name__]
try:
    logfile = open("logs/std.log-" + str(time.time()).strip(" "), 'w')
except Exception as e:
    print("Error opening log file!\n\n", e)
    raise SystemExit(1)

def log(input):
    logfile.write(f"\n[{str(time.time()).strip(' ')}]\n{str(input)}\n")
    
def cleanup():
    logfile.close()
    

try:
    with open('pyserver.conf', 'r') as f:
        conf = f.readlines()
        host = conf[0].strip()
        port = int(conf[1].strip())
        version = str(conf[2].strip())
        sourcefile = str(conf[3].strip())
        verbosity = int(conf[4].strip())
        maxreplog = int(conf[5].strip())
    f.close()
    if(verbosity >= 1):
        print("Read config file successfully!")
    
except Exception as e:
    print("Error reading pyserver.conf!\n\n", e)
    raise SystemExit(1)

try:
    with open(sourcefile, 'r') as f:
        source = f.read()
    f.close()
    if(verbosity >= 1):
        print("Read server content successfully!")
    
except Exception as e:
    print("Error reading server content!\n\n", e)
    raise SystemExit(1)    
    
    
def TCPstart():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # so it doesn't hog that port for another minute after the program ends
    sock.bind((host, port))
    sock.listen(5) # normal max is 5 users queued
    if(verbosity >= 1):
        print("Listening on ", sock.getsockname())
    while True:
        user, addr = sock.accept()
        log(f"{user} connected, time = {str(time.time())}")
        if(verbosity == 2):
            print(user, " connected, time =", time.time())
        elif(verbosity == 1):
            print("new connection, time =", time.time())
        data = user.recv(4096) # read first 4K of data
        user.sendall(handler(data))
        
        user.close()
        log(f"connection closed, time =, {str(time.time())}")
        if(verbosity == 2):
            print("connection closed, time =", time.time())
        elif(verbosity == 1):
            print("connection closed")
class Request:
    def __init__(self, data):
        self.method = None
        self.uri = None
        self.http_version = "1.1"
        self.path = None
        self.params = None
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
        self.path = self.uri.split("?", 1)[0].strip('/')

        try:
            self.params = dict(item.split('=') for item in self.uri.split('?',1)[1].split('&') if item)
        except:
            self.params = ""
        print(str(self.method + "\n" + self.uri + "\n" + self.http_version + "\n" + self.path + "\n" + str(self.params)))
        log(str("\n" + self.method + "\n" + self.uri + "\n" + self.http_version + "\n" + self.path + "\n" + str(self.params) + "\n"))


            

def handler_HEAD(request):
    type = "text/html"
    loc = request.path

    file_size = 696969
    if(os.path.exists(loc)):
        file_size = os.path.getsize(loc)
        response = b"HTTP/1.1 200 OK\r\n"
        with open(loc, 'rb') as file:
            body = file.read()
            type = mimetypes.guess_type(loc)[0] or 'text/html'
        
    else:
        response = b"HTTP/1.1 404 Not Found\r\n"
        body = b"<b><h1>HTTP 404: Not Found</b></h1><br><br><p>(C) 2023 Killaship, pyserver project<br><a href='https://github.com/Killaship/pyserver'>github link</a></p>"
    
    header = b"".join([
        bytes(str("Server: pyserver"+version+"\r\n"), 'utf-8'),
        bytes(str("Content-Type: "+type+"\r\n"), "utf-8"), 
        b"Access-Control-Allow-Origin: *\r\n"
    ])
    bline = b"\r\n"

    if(verbosity == 2):
        if(file_size < maxreplog):  # if file size is under max allowed to print
            log(f"response:\n{str(response+header)}\n")
            print("response:\n"+str(response+header)+"\n")
        else:
            log(f"response:\n{str(response+header)}\n")
            print("response:\n"+str(response+header)+"\n")
    elif(verbosity == 1):
        print("responded")    
    
    return b"".join([response, header]) # HEAD requests don't have bodies, but they return headers as if they were a GET request
            
            
def handler_GET(request):
    type = "text/html"
    loc = request.path
    file_size = 696969
    if(os.path.exists(loc)):
        file_size = os.path.getsize(loc)
        response = b"HTTP/1.1 200 OK\r\n"
        with open(loc, 'rb') as file:
            body = file.read()
            type = mimetypes.guess_type(loc)[0] or 'text/html'
        
    else:
        response = b"HTTP/1.1 404 Not Found\r\n"
        body = b"<b><h1>HTTP 404: Not Found</b></h1><br><br>" #<p>pyserver project<br><a href='https://github.com/Killaship/pyserver'>github link</a></p>"
    
    header = b"".join([
        bytes(str("Server: pyserver"+version+"\r\n"), 'utf-8'),
        bytes(str("Content-Type: "+type+"\r\n"), "utf-8"), 
        b"Access-Control-Allow-Origin: *\r\n"
    ])
    bline = b"\r\n"

    if(verbosity == 2):
        if(file_size < maxreplog):  # if file size is under max allowed to print
            log(f"response:\n{str(response+header+bline+body)}\n")
            print("response:\n"+str(response+header+bline+body)+"\n")
        else:
            log(f"response:\n{str(response+header+bline+body[0:maxreplog])}[rest truncated for size]\n")
            print("response:\n"+str(response+header+bline+body[0:maxreplog])+"[rest truncated for size]\n")
    elif(verbosity == 1):
        print("responded")    

    
    return b"".join([response, header, bline, body])
        

def handler_501(request):
    response = b"HTTP/1.1 501 Not Implemented\r\n"
    header = b"".join([
        bytes(str("Server: pyserver"+version+"\r\n"), 'utf-8'),
        b"Content-Type: text/html\r\n", b"Access-Control-Allow-Origin: *\r\n"
    ])
    bline = b"\r\n"
    body = b"<b><h1>HTTP 501: Not Implemented</b></h1><br><br><p>(C) 2023 Killaship, pyserver project<br><a href='https://github.com/Killaship/pyserver'>github link</a></p>"
    
    if(verbosity == 2):
        log(f"response:\n{str(response+header+bline+body)}\n")
        print("response:\n"+str(response+header+bline+body)+"\n")
    elif(verbosity == 1):
        print("responded")

    return b"".join([response, header, bline, body])

def handler_OPTIONS(request): 
    response = b"HTTP/1.1 200 OK\r\n"
    header = b"".join([
        bytes(str("Server: pyserver"+version+"\r\n"), 'utf-8'),
        b"Content-Type: text/html\r\n", bytes(implementedmethods, 'utf-8'), 
        b"Access-Control-Allow-Origin: *\r\n"
    ])
    bline = b"\r\n"
    body = b""
    
    
    if(verbosity == 2):
        log(f"response:\n{str(response+header+bline+body)}\n")
        print("response:\n"+str(response+header+bline+body)+"\n")
    elif(verbosity == 1):
        print("responded")
        
    return b"".join([response, header, bline, body])

def handler(data):   
    request = Request(data)
    if(verbosity == 2):
        print("new request:\n"+str(data))
    elif(verbosity == 1):
        print("new request")
    log(str("new request:\n"+str(data)))
    try:
        methodhandler = getattr(current_module, 'handler_%s' % request.method) # useful hack I found
    except AttributeError:
        methodhandler = handler_501
    response = methodhandler(request)
    

    return response




if __name__ == '__main__':
    try:
        TCPstart()
    except KeyboardInterrupt:
        if(verbosity >= 1):
            print("\nserver exited, cleaning up\n")
        log("\nserver exited, cleaning up\n")
        cleanup()
