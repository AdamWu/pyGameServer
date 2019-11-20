#coding:utf-8
import socket,struct
import threading,time,random

# proto
from pb2 import Login_pb2
from pb2 import Position_pb2

class Client(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self)
        self.server_host = args[0]
        self.server_port_tcp = args[1]
        self.server_port_udp = args[2]
    
    def run(self):
        self.connect()
        self.login()
        while True:
            # receive data      
            dataLength = 0
            data = b''
            try:
                buff = self.sock_tcp.recv(1024)
            except Exception as e:
                print("Error : %s" % str(e))
                self.sock_tcp.close()
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
            
            self.sync_move()

            time.sleep(0.1)

    # connect server
    def connect(self):
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect((self.server_host,self.server_port_tcp))

    # 接受数据
    def receive(self, bytes):
        key = struct.unpack('!H', bytes[0:2])[0]
        data = bytes[2:]
        print ('receive {0}'.format(key))
        if key == 1001:
            self.login_callback(data)
        elif key == 2001:
            self.sync_move_callback(data)
        
    # 发送数据
    def send(self, protocal, bytes):
        print ('send {0}'.format(protocal))
        data = struct.pack('!iH', 2+len(bytes), protocal)
        data += bytes
        try:
            self.sock_tcp.sendall(data)
        except Exception as e:
            print("Error : %s" % str(e))
        
    def login(self):
        req = Login_pb2.LoginReq()
        req.login.UserName = "adamwu"
        self.send(1000, req.SerializeToString())
    def login_callback(self, bytes):
        res = Login_pb2.LoginRes()
        res.ParseFromString(bytes)
        print ('login success, uid:{0}'.format(res.userId))
    def sync_move(self):
        req = Position_pb2.PosReq()
        req.position.x = random.random()
        req.position.y = random.random()
        req.position.z = random.random()
        self.send(2000, req.SerializeToString())
    def sync_move_callback(self, bytes):
        res = Position_pb2.PosRes()
        res.ParseFromString(bytes)
        print ("sync_move_callback uid:{0}".format(res.uid))


if __name__ == "__main__":
    clients = [0 for i in range(1)]
    for i in range(1):
        clients[i] = Client(["127.0.0.1", 8001, 8001])
        clients[i].start()

   
    
