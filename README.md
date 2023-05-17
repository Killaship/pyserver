# pyserver
A simple HTTP server written in Python.

<img width="244" alt="image" src="https://github.com/Killaship/pyserver/assets/69988679/cc924298-6889-4e7e-8a95-b57add1c49f0">

It can load content to be served from a file, and it also gets the location of that stuff from the configuration file.

See the configuration guide for more on how to use that.

Run ```sudo python3 main.py``` to run the web server. (You might not need the sudo on your system, but I did when I tested it.)

Some tools that could work to test the implementation of HTTP are these: 
- https://reqbin.com
- https://resttesttest.com
- https://hurl.dev


I'm not sponsored or endorsed by them or anything, but I found them off google, and they look good to me.

# Configuration Guide
The config file reads its settings based off what line the parameter is on. For example, the second line should contain the port to run the server on.

Here's a full overview:

- The first line is the address to host the server on. 
- The second line is the port to run the server on.
- Third line is the server version, which goes in the HTTP response sent to clients.
- The fourth line contains the location of the source file to be served.
- The fifth line contains the verbosity level of the server program. 2 is full debug, everything printed out. 1 is basic logging. 0 prints out nothing at all, besides errors. Regardless of verbosity settings, the program will still log at full verbosity in its log files.

Please see the text files under ```logs/examples``` for examples of the server verbosity settings.
