# -*- coding: utf-8 -*-
import struct

class ByteArray:
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.length = len(data)

    def readByte(self):
        newPos = self.pos + 1
        if newPos <= self.length:
            value = struct.unpack('!b', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print 'index out of boundary'

    def readShort(self):
        newPos = self.pos + 2
        if newPos <= self.length:
            value = struct.unpack('!h', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print 'index out of boundary'

    def readUShort(self):
        newPos = self.pos + 2
        if newPos <= self.length:
            value = struct.unpack('!H', self.data[self.pos:newPos])
            self.pos = newPos
            return value[0]
        else:
            print 'index out of boundary'

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

    def readString(self):
        newPos=self.pos + 2
        if newPos<=self.length:
            stringLength=struct.unpack('!H',self.data[self.pos:newPos])[0]
            form='!'+str(stringLength)+'s'
            value=struct.unpack(form,self.data[newPos:newPos+stringLength])
            self.pos=newPos+stringLength
            return value[0]
        else:
            print 'index out of boundary'

    def readBytes(self):
        newPos=self.pos + 2
        if newPos<=self.length:
            stringLength=struct.unpack('!H',self.data[self.pos:newPos])[0]
            form='!'+str(stringLength)+'s'
            value=struct.unpack(form,self.data[newPos:newPos+stringLength])
            self.pos=newPos+stringLength
            return value[0]
        else:
            print 'index out of boundary'
