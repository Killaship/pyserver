# pyserver
A simple HTTP server written in Python.

<img width="244" alt="image" src="https://github.com/Killaship/pyserver/assets/69988679/cc924298-6889-4e7e-8a95-b57add1c49f0">

It can load content to be served from a file, and it also gets the location of that stuff from the configuration file.

The config file reads stuff based off lines. 
The first line is the address to host the server on. Second line is the port.
Third line is the server version, and the last line is the location of the source file to be served.

The server version is A, nice to know, and B, goes in the HTTP response sent to a client.

Run ```sudo python3 main.py``` to run the web server. (You might not need the sudo on your system, but I did when I tested it.)

Some tools that could work to test the implementation of HTTP are these: 
- [https://reqbin.com/]
- [https://resttesttest.com/]
- [https://hurl.dev/]
I'm not sponsored or endorsed by them or anything, but I found them off google, and they look good to me.
