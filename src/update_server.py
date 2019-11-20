#!/usr/bin/python

'''
	upadate server	
'''
import http.server
import socketserver

import config

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", config.UPDATE_SERVER_PORT), Handler) as httpd:
    print("upadate server start at port:", config.UPDATE_SERVER_PORT)
    httpd.serve_forever()
    print ("ok")
