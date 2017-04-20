# -*- coding: utf-8 -*-

import SocketServer
import struct
import time
import sys
import json

from config import *

from network import *

# proto
from pb2 import logic_pb2
from pb2 import main_pb2


CFG = {}
CFG['items'] = {}
CFG['equips'] = {}
data = json.load(file('../cfg/item.json'))
for id in data:
        CFG['items'][int(id)] = data[id]
data = json.load(file('../cfg/equip.json'))
for id in data:
        CFG['equips'][int(id)] = data[id]


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

        # 处理数据
        def handleData(self, byteArray):
                key = byteArray.ReadUShort()
                print 'handleData', key
                if key == REQ_LOGIN:
                        self.onLogin(byteArray)
                elif key == REQ_ENTER:
                        self.onEnter(byteArray)
                elif key == REQ_SELL:
                        self.onSell(byteArray)

        def sendData(self, data):
                form='!H'+str(len(data))+'s'
                self.request.sendall(struct.pack(form, len(data), data))

        def onLogin(self, byteArray):
                login = logic_pb2.LoginRequest()
                login.ParseFromString(byteArray.ReadBytes())
                print 'onLogin', login.name, login.pwd
                global gUserCount
                gUserCount = gUserCount + 1
                self._userid = gUserCount
                gSessionList[self._userid] = self

                user = main_pb2.User()
                user.id = str(self._userid)
                user.name = login.name
                user.lv = 10
                user.exp = 200
                user.cash = 30
                user.coin = 12390
                for id in CFG['items']:
                        if id >= 100:        
                                user.item.add(id=id, num=1000)
                data = user.SerializeToString()
                byteData = struct.pack('!H', ACK_LOGIN)
                byteData += struct.pack('!H'+str(len(data))+'s', len(data), data)
                self.sendData(byteData)

        def onEnter(self, byteArray):
                print 'onEnter'
                byteData = struct.pack('!H', ACK_ENTER)
                self.sendData(byteData)

        def onSell(self, byteArray):
                id = byteArray.ReadInt()
                print 'onSell', id
                byteData = struct.pack('!H', ACK_SELL)
                byteData += struct.pack('!i', id)
                self.sendData(byteData)



myServer = SocketServer.ThreadingTCPServer((GAME_SERVER_IP,GAME_SERVER_PORT), MyHandler)
print 'server started ...'
myServer.serve_forever()
