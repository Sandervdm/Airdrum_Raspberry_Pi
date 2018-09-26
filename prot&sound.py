# import library
import serial
import pygame
import os

class protocol:
    # create a handle for the serial port
    ser = serial.Serial()

    # create variables
    datatype = 0
    dataarray = []

    def __init__(self):
        self.ser.baudrate = 9600
        self.ser.timeout = 0.05
        self.ser.port = "/dev/ttyAMA0"
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
            self.ser.write(sendarray)
            return True
        else:
            return False

    def receive(self):
        try:
            del self.dataarray[:]
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
        except Exception as eee:
            return False
            #print("Receiving gave an error" + str(eee))

    def close(self):
        self.ser.close()

#protocol example
#ProtHandle = protocol()
#senddata = [0,0,255,100,0,0,255,100,0,0,255,100,0,0,255,100,0,0,255,100]
#ProtHandle.transmit(10, senddata)

ProtHandle = protocol()

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()
pygame.init()

sndPa = pygame.mixer.Sound("sounds/piano/a.wav")
sndPb = pygame.mixer.Sound("sounds/piano/b.wav")
sndPc = pygame.mixer.Sound("sounds/piano/c.wav")
sndPd = pygame.mixer.Sound("sounds/piano/d.wav")
sndPe = pygame.mixer.Sound("sounds/piano/e.wav")
sndPf = pygame.mixer.Sound("sounds/piano/f.wav")

sndDa = pygame.mixer.Sound("sounds/drums/Claves.wav")
sndDb = pygame.mixer.Sound("sounds/drums/Snare.wav")
sndDc = pygame.mixer.Sound("sounds/drums/Kick.wav")
sndDd = pygame.mixer.Sound("sounds/drums/Tom.wav")
sndDe = pygame.mixer.Sound("sounds/drums/Clap.wav")
sndDf = pygame.mixer.Sound("sounds/drums/Crash.wav")

soundChannelA = pygame.mixer.Channel(1)

switchBool = false

while True:
    if ProtHandle.receive():
        if ProtHandle.datatype == 11:
            #schijtdata omvormen
            integerValue = int(ord(ProtHandle.dataarray[0]))
            #controleren welke toets is ingedrukt
			if integerValeu == 63:
				#change instrument
				switchBool = not(switchBool)
			else:
				if switchBool == false:
					if integerValue & 1:
						soundChannelA.play(sndPa)
					if integerValue & 2:
						soundChannelA.play(sndPb)
					if integerValue & 4:
						soundChannelA.play(sndPc)
					if integerValue & 8:
						soundChannelA.play(sndPd)
					if integerValue & 16:
						soundChannelA.play(sndPe)
					if integerValue & 32:
						soundChannelA.play(sndPf)
				else:
					if integerValue & 1:
						soundChannelA.play(sndDa)
					if integerValue & 2:
						soundChannelA.play(sndDb)
					if integerValue & 4:
						soundChannelA.play(sndDc)
					if integerValue & 8:
						soundChannelA.play(sndDd)
					if integerValue & 16:
						soundChannelA.play(sndDe)
					if integerValue & 32:
						soundChannelA.play(sndDf)
			