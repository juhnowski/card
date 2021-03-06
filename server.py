#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import RPi.GPIO as GPIO

from time import sleep

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        with open ("keyboard.html", "r") as myfile:
            data=myfile.readlines()
        self.wfile.write(data)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
	GPIO.output(7,False)
	sleep(1.50)
	GPIO.output(8,True)
	sleep(1.50)
        self.wfile.write("<html><body><h1>DONE!</h1><br> Then som activate process start</body></html>")

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(7,GPIO.OUT)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(8,GPIO.OUT)

    GPIO.output(7,True)
    sleep(1.50)
    GPIO.output(8,True)
    sleep(1.50)

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
