# -*- coding: utf-8 -*-

'''
	a simple http server
	
'''
import SimpleHTTPServer
import SocketServer


Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(('', 8000), Handler)
httpd.serve_forever()
