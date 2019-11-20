#!/usr/bin/python

import socketserver
import struct
import time
import sys
import json

from config import *

from network import ByteArray

# proto
from pb2 import Login_pb2
from pb2 import Position_pb2

ClientList = {}
gid = 1
gUsers = {}

def sendToAll(protocal, bytes):
    for client in ClientList.values():
        client.send(protocal, bytes)

def sendToAllExcept(protocal, bytes, uid):
    for client in ClientList.values():
        if client.uid != uid:
            client.send(protocal, bytes)

# 每一个请求都会实例化
class MyHandler(socketserver.BaseRequestHandler):

    def init(self):
        self.username = ""
        self.uid = 0

    def finish(self):
        if gUsers.get(self.username) != None:
            del gUsers[self.username]
        if gUsers.get(self.uid) != None:
            del ClientList[self.uid]
        print ('client disconnected:', self.client_address)

    def handle(self):
        self.init()
        print ('client connected:', self.client_address)
        dataLength = 0
        data = b''
        while True:
            try:
                buff = self.request.recv(1024)
            except Exception as e:
                print("Error : %s" % str(e))
                self.request.close()
                break

            data+=buff

            # header not ok
            if dataLength == 0 and len(data) < 4: 
                continue

            # header ok
            if dataLength == 0:
                dataLength = struct.unpack('!i', data[0:4])[0]

            # message ok
            while len(data) >= dataLength+4:
                self.receive(data[4:dataLength+4])
                data = data[dataLength+4:]
                dataLength = 0
                if len(data) >= 4:
                        dataLength = struct.unpack('!i', data[0:4])[0]

    # 接受数据
    def receive(self, bytes):
        key = struct.unpack('!H', bytes[0:2])[0]
        data = bytes[2:]
        print ('receive {0} {1}'.format(self.client_address, key))
        if key == 1000:
            self.login(data)
        else:
            # 未登录
            if self.uid == 0:
                return
            req = Position_pb2.PosReq()
            req.ParseFromString(data)
            res = Position_pb2.PosRes()
            res.uid = self.uid
            res.position.x = req.position.x
            res.position.y = req.position.y
            res.position.z = req.position.z
            sendToAll(key+1, res.SerializeToString())
    # 发送数据
    def send(self, protocal, bytes):
        #print ('send {0}'.format(protocal))
        data = struct.pack('!iH', 2+len(bytes), protocal)
        data += bytes    
        try:
            self.request.sendall(data)  
        except Exception as e:
            print("Error : %s" % str(e))
            self.finish()


    def login(self, bytes):
        loginreq = Login_pb2.LoginReq()
        loginreq.ParseFromString(bytes)
        username = loginreq.login.UserName
        print("user login {0}".format(loginreq.login.UserName))

        global gid
  
        # 查找当前用户
        if gUsers.get(username) != None:
            uid = gUsers[username]
            client = ClientList.get(uid)
            if client != None:
                client.finish()
            # 踢掉当前用户
            ClientList[uid] = self
            print("kick user:{0} id:{1}".format(username, gid))
        else:
            # 新用户
            gid = gid + 1
            gUsers[username] = gid
            ClientList[gid] = self
            print("new user:{0} id:{1}".format(username, gid))
          
        self.username = username
        self.uid = gid  

        loginrep = Login_pb2.LoginRes()
        loginrep.msgCode = 0
        loginrep.userId = self.uid
        self.send(1001, loginrep.SerializeToString())    



myServer = socketserver.ThreadingTCPServer(("",GAME_SERVER_PORT), MyHandler)
print("tcp server start at port:", GAME_SERVER_PORT)
myServer.serve_forever()
