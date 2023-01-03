import serial 

import time 

class Neulog(object):
    def __init__(self, port, baud):
        self.ser = serial.Serial(port=port, baudrate=baud)
        self.status = 'connected'
        self.buf = []
        t = time.time()
        while not self.connect():
            if time.time() - t > 2:
                break
    
    def send(self, s, checksum=False):
        time.sleep(0.02)
        self.ser.flushInput()
        self.ser.flushOutput()
        for c in s:
            self.ser.write(c.encode())
        if checksum:
            self.ser.write(chr(sum([ord(c) for c in s]) % 256).encode())
    
    def receive(self, i=False):
        time.sleep(0.02)
        iw = self.ser.inWaiting()
        if False == i:
            i = iw
        print(self.ser.read(1))
        if iw >= i:
            r = self.ser.read(i)
            print("R", r)
            return r
        return 'False'
    
    def connect(self):
        self.ser.close()
        self.ser.open()
        self.send(chr(85) + 'NeuLog!')
        if 'OK-V' != self.receive(4):
            return False
        self.status = 'connected'
        return '.'.join([str(ord(c)) for c in self.ser.receive(3)])
    
    def scanStart(self):
        if self.status != 'connected':
            return False
        self.send(chr(18) + chr(96) + chr(34) + chr(9), True)
        r = self.receive(4)
        print("Scan start r", r)
        print("What's this: %i" % (ord(r[-1])))
        if chr(18) + chr(96) + chr(11) == r[:-1]:
            self.status = 'scanning'
            return True
        return False
    
    def scanRead(self):
        if self.status != 'scanning':
            return False
        sensors = []
        r = self.receive()
        while len(r) > 7:
            chunk, r = r[:8], r[8:]
            if chr(85) != chunk[0]:
                continue
            chunk = [ord(c) for c in chunk]
            check = chunk[-1] != sum(chunk[:-1]) % 256
            if check:
                continue
            stype, sid, ssndver = chunk[1:4]
            sver = '.'.join([str(i) for i in chunk[4:7]])
            sensors.append((stype, sid, sver))
        return sensors
    
    def scan(self):
        t = time.time()
        sensors = []
        self.scanStart()
        time.sleep(1)
        sensor = self.scanRead()
        while len(sensor) != 0:
            sensors += sensor
            sensor = self.scanRead()
        self.scanStop()
        self.sensors = sensors
    
    def scanStop(self):
        if self.status != 'scanning':
            return False
        self.send(chr(18))
        self.receive()
        self.status = 'connected'
        return True
    
    def getSensorsData(self, stype, sid):
        if self.status != 'connected':
            return False
        self.send(chr(85) + chr(stype) + chr(sid) + chr(49) + (3 * chr(0)), True)
        r = self.receive()
        print("R", r)
        if not r or chr(85) != r[0] or chr(49) != r[3]:
            return False
        r = [ord(c) for c in r]
        if r[-1] != sum(r[:-1]) % 256:
            return False
        return r
    
    def read(self):
        data = []
        for stype, sid, vid in self.sensors:
            x = self.device.getSensorsData(stype, sid)
            data.append(x)
        return data