# -*- coding: utf-8 -*-

import SocketServer
import struct
import time
import sys

from level import GameLevel

OPCODE_REQ_LOGIN = 1
OPCODE_REQ_SYNCTIME1 = 2
OPCODE_REQ_SYNCTIME2 = 3
OPCODE_REQ_ENTERCITY = 4
OPCODE_REQ_ENTERLEVEL = 5
OPCODE_REQ_MOVE = 11
OPCODE_REQ_STOP	= 12

OPCODE_ACK_LOGIN = 10001
OPCODE_ACK_SYNCTIME1 = 10002
OPCODE_ACK_SYNCTIME2 = 10003
OPCODE_ACK_ENTERCITY = 10004
OPCODE_ACK_ENTERLEVEL = 10005
OPCODE_ACK_MOVE = 10011
OPCODE_ACK_STOP	= 10012

def caculate_length(info):
    a={'i':4,'s':1,'h':2,'d':8,'f':4}
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

class ByteArray:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.length = len(data)

    def readInt(self):
        newPos = self.pos + 4
        if newPos <= self.length:
            value = struct.unpack('!i', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print 'index out of boundary'

    def readFloat(self):
        newPos = self.pos + 4
        if newPos <= self.length:
            value = struct.unpack('!f', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print 'index out of boundary'

    def readDouble(self):
        newPos = self.pos + 8
        if newPos <= self.length:
            value = struct.unpack('!d', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print 'index out of boundary'

    def readstring(self):
        newPos=self.pos+2
        if newPos<=self.length:
            stringLength=struct.unpack('!h',self.data[self.pos:newPos])
            form='!'+str(stringLength)+'s'
            value=struct.unpack(form,self.data[newPos:newPos+stringLength])
            self.pos=newPos+stringLength
            print value
        else:
            print 'index out of boundary'


gSessionList = {}
gUserCount = 0
gGameLevel = GameLevel()


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
                                dataLength = struct.unpack('!i', data[0:4])[0]

                        while len(data) >= dataLength + 4:
                                self.handleData(ByteArray(data[4:dataLength+4])) # process data
                                data = data[dataLength+4:]
                                dataLength = 0
                                if len(data) >= 4:
                                        dataLength = struct.unpack('!i', data[0:4])[0]

        def ct2st(ct): # client time to server time
                return ct + self._timeDelta

        def onLogin(self):
                global gUserCount
                gUserCount = gUserCount + 1
                self._userid = gUserCount
                gSessionList[self._userid] = self
                byteData = struct.pack('!iii', caculate_length('!ii'), OPCODE_ACK_LOGIN, self._userid)
                self.request.sendall(byteData)

        def onSyncTime1(self, ct1):
                print 'onSyncTime1'
                byteData = struct.pack('!iidd', caculate_length('!idd'), OPCODE_ACK_SYNCTIME1, ct1, time.time())
                self.request.sendall(byteData)


        def handleData(self, bArray):
                key = bArray.readInt()
                if key == OPCODE_REQ_LOGIN:
                        self.onLogin()
                elif key == OPCODE_REQ_SYNCTIME1:
                        self.onSyncTime1(bArray.readDouble())


myServer = SocketServer.ThreadingTCPServer(('',8001), MyHandler)
print 'server started ...'
myServer.serve_forever()
