# -*- coding: utf-8 -*-

import SocketServer
import struct
import time
import sys
from ByteArray import *

REQ_LOGIN = 1001
ACK_LOGIN = 1002
REQ_ENTER = 1003
ACK_ENTER = 1004

def caculate_length(info):
    a={'i':4,'s':1,'h':2,'H':2,'d':8,'f':4}
    b=[]
    for i in info:
       if i in a:
           b.append(a[i])
       elif i.isdigit():
           b.append(int(i)-1)

    x=0
    for i in b:
        i=i+x
        x=i
    return x

gSessionList = {}
gUserCount = 0

def sendToAll(byteData):
        for session in gSessionList.values():
                session.request.sendall(byteData)


class MyHandler(SocketServer.BaseRequestHandler):

        def init(self):
                self._netDelay = 0
                self._timeDelta = 0
                self._userid = -1

        def finish(self):
                if self._userid > 0:
                        del gSessionList[self._userid]

        def handle(self):
                print '...connected from:', self.client_address
                dataLength = 0
                data = ''
                self.init()
                while 1:
                        buff = self.request.recv(1024)
                        count = len(buff)
                        if count == 0:
                                continue
                        print 'data reveived:', count

                        data+=buff

                        if dataLength == 0:
                                dataLength = struct.unpack('!H', data[0:2])[0]

                        while len(data) >= dataLength+2:
                                self.handleData(ByteArray(data[2:dataLength+2])) # process data
                                data = data[dataLength+2:]
                                dataLength = 0
                                if len(data) >= 2:
                                        dataLength = struct.unpack('!H', data[0:2])[0]

        def ct2st(ct): # client time to server time
                return ct + self._timeDelta


        # 处理数据
        def handleData(self, bArray):
                key = bArray.readUShort()
                print 'handleData', key
                if key == REQ_LOGIN:
                        self.onLogin(bArray.readString(), bArray.readString())
                elif key == REQ_ENTER:
                        self.onEnter()

        def sendData(self, data):
                form='!H'+str(len(data))+'s'
                self.request.sendall(struct.pack(form, len(data), data))

        def onLogin(self, name, pwd):
                print 'onLogin', name, pwd
                global gUserCount
                gUserCount = gUserCount + 1
                self._userid = gUserCount
                gSessionList[self._userid] = self
                byteData = struct.pack('!H', ACK_LOGIN)
                byteData += struct.pack('!i', self._userid)
                byteData += struct.pack('!H'+str(len(name))+'s', len(name), name)
                byteData += struct.pack('!f', 12.9)
                self.sendData(byteData)

        def onEnter(self):
                print 'onEnter'
                byteData = struct.pack('!H', ACK_ENTER)
                self.sendData(byteData)



myServer = SocketServer.ThreadingTCPServer(('',8001), MyHandler)
print 'server started ...'
myServer.serve_forever()
