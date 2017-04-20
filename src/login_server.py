# -*- coding: utf-8 -*-

'''
	a simple http server
	
'''
import SimpleHTTPServer
import SocketServer

from config import *

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer((LOGIN_SERVER_IP, LOGIN_SERVER_PORT), Handler)
httpd.serve_forever()
