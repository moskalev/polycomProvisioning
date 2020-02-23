#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import datetime
import os


class S(BaseHTTPRequestHandler):
    def __init__(self, *args, log_file = 'polycom.log', **kwargs):
        self.log_file = log_file
        super(S, self).__init__(*args, **kwargs)
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        self._set_headers()
        fname =  str(self.path).split('/')[-1]
        if os.path.exists('files/' + fname):
            print('Serving ', fname)
            with open('files/' + fname, 'rb') as file: 
                self.wfile.write(file.read())
        else:
            print('Not found ', fname) # Do not reply with an error here

    def do_POST(self):
        with open(self.log_file, "a") as f:
            '''Reads post request body'''
            self._set_headers()
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            f.write("\n")
            f.write(str(self.headers))
            post_body = self.rfile.read(int(self.headers['Content-Length'])).decode("UTF-8")
            f.write(str(post_body))
            f.write("\n")

    def do_PUT(self):
        self.do_POST()

def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd... on port', port)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
