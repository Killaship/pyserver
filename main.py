import socket

class TCP:
    host = '127.0.0.1' # TODO: Replace host and port values with those from a config file
    port = 80
    def TCPstart():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(TCP.host, TCP.port)
        s.listen(5) # normal max is 5 users queued
        print("Listening on ", s.getsockname())
        while True:
            user = s.accept()
            print(user, " connected")
            data = user.recv(4096) # read first 4K of data
            user.sendall(data) # echo everything back

            
if __name__ == '__main__':
    TCP.TCPstart()

