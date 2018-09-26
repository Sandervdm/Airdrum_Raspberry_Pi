# import library
import serial

class protocol:
    # create a handle for the serial port
    ser = serial.Serial()

    # create variables
    datatype = 0
    dataarray = []

    def __init__(self):
        self.ser.baudrate = 9600
        self.ser.timeout = 0.05
        self.ser.port = "COM7"  # "/dev/ttyAMA0"
        try:
            self.ser.open()
            print("Connected to: " + self.ser.name)
        except:
            print("Failed to connect to: " + self.ser.name)

    def transmit(self, type, data):
        if self.ser.is_open:
            check = 85 + type + len(data)
            sendarray = []
            sendarray += chr(85)
            sendarray += chr(len(data))
            sendarray += chr(type)
            for d in data:
                sendarray += chr(d)
                check += d
            check = ~check
            sendarray += chr(check % 0xFF)
            #TODO: controleren kut
            self.ser.write(sendarray)
            return True
        else:
            return False

    def receive(self):
        try:
            if self.ser.is_open:
                startbyte = self.ser.read()
                if ord(startbyte) == 85:
                    length = ord(self.ser.read())
                    self.datatype = ord(self.ser.read())
                    for i in range(0, length):
                        self.dataarray += self.ser.read()
                    check = ord(self.ser.read())
                    return True
                else:
                    self.ser.flushInput()
                    return False
            else:
                return False
        except:
            print("Receiving gave an error")

    def close(self):
        self.ser.close()

#protocol example
ProtHandle = protocol()
senddata = [0,0,255,100,0,0,255,100,0,0,255,100,0,0,255,100,0,0,255,100]
ProtHandle.transmit(10, senddata)
if ProtHandle.receive():
    print(ProtHandle.datatype)
    print(ProtHandle.dataarray)
else:
    print("Nothing received. Probably a timeout.")

#bit test example
#test = 56
#for i in range(0, 8):
#    if test & (1<<i):
#        print("ja")
#    else:
#        print("nee")
