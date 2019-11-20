#!/usr/bin/python

'''
	a simple http server	
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import io,shutil  
import urllib

import config

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        data = {'ret':1, 'data':{'name':'wu', 'id':11}} 

        self.wfile.write(json.dumps(data).encode())

if __name__ == '__main__':
    server = HTTPServer(("", config.LOGIN_SERVER_PORT), Resquest)
    print("upadate server start at port:", config.LOGIN_SERVER_PORT)
    server.serve_forever()
