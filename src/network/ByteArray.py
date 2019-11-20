# -*- coding: utf-8 -*-
import struct

class ByteArray:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.length = len(data)

    def ReadByte(self):
        newPos = self.pos + 1
        if newPos <= self.length:
            value = struct.unpack('!b', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print ('index out of boundary')

    def ReadShort(self):
        newPos = self.pos + 2
        if newPos <= self.length:
            value = struct.unpack('!h', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print ('index out of boundary')

    def ReadUShort(self):
        newPos = self.pos + 2
        if newPos <= self.length:
            value = struct.unpack('!H', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print ('index out of boundary')

    def ReadInt(self):
        newPos = self.pos + 4
        if newPos <= self.length:
            value = struct.unpack('!i', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print ('index out of boundary')

    def ReadFloat(self):
        newPos = self.pos + 4
        if newPos <= self.length:
            value = struct.unpack('!f', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print ('index out of boundary')

    def ReadDouble(self):
        newPos = self.pos + 8
        if newPos <= self.length:
            value = struct.unpack('!d', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print ('index out of boundary')

    def ReadString(self):
        newPos=self.pos + 4
        if newPos<=self.length:
            stringLength=struct.unpack('!i',self.data[self.pos:newPos])[0]
            form='!'+str(stringLength)+'s'
            value=struct.unpack(form,self.data[newPos:newPos+stringLength])
            self.pos=newPos+stringLength
            return value[0]
        else:
            print ('index out of boundary')

    def ReadBytes(self):
        newPos=self.pos + 2
        if newPos<=self.length:
            stringLength=struct.unpack('!H',self.data[self.pos:newPos])[0]
            form='!'+str(stringLength)+'s'
            value=struct.unpack(form,self.data[newPos:newPos+stringLength])
            self.pos=newPos+stringLength
            return value[0]
        else:
            print ('index out of boundary')
