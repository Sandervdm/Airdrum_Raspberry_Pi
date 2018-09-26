# import library
import serial
import sched
import time
import threading
import pygame
import os

class protocol:
    # create a handle for the serial port and initialize variables
    ser = serial.Serial()
    datatype = 0
    dataarray = []

    def __init__(self):
        #initialiseer systeem
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
            #vul checkvalue met data
            check = 85 + type + len(data)
            #vul array met data
            sendarray = []
            sendarray += chr(85)
            sendarray += chr(len(data))
            sendarray += chr(type)
            for d in data:
                sendarray += chr(d)
                check += d
            check = ~check
            sendarray += chr(check % 0xFF)
            #verzend data
            self.ser.write(sendarray)
            return True
        else:
            return False

    def receive(self):
        try:
            #leeg data array
            del self.dataarray[:]
            #controleer of startbyte in orde is
            startbyte = self.ser.read()
            if ord(startbyte) == 85:
                #lees datalengte
                length = ord(self.ser.read())
                #lees datatype
                self.datatype = ord(self.ser.read())
                #lees alle data
                for i in range(0, length):
                    self.dataarray += self.ser.read()
                #lees de checkbyte
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
		
		
def MusicFunction(*args):
	switchBool = False
	oldvalue = 0
	while True:
	    if ProtHandle.receive():
            if ProtHandle.datatype == 11:
                #data omvormen
                integerValue = int(ord(ProtHandle.dataarray[0]))
                if integerValue == 51:
                    #Verander instrument als de vier buitenste panelen aan staan
                    switchBool = not(switchBool)
                else:
                    #filter alle panelen die al aanstaan er uit
                    andvalue = oldvalue & integerValue
                    andvalue = ~andvalue
                    integerValue &= andvalue
                    #speel muziek af aan de hand van ontvangen waarde en gekozen instrument
                    if switchBool == False:
                        if integerValue & 1:
                            soundChannelA.play(sndPa)
                        if integerValue & 2:
                            soundChannelB.play(sndPb)
                        if integerValue & 4:
                            soundChannelC.play(sndPc)
                        if integerValue & 8:
                            soundChannelD.play(sndPd)
                        if integerValue & 16:
                            soundChannelE.play(sndPe)
                        if integerValue & 32:
                            soundChannelF.play(sndPf)
                    else:
                        if integerValue & 1:
                            soundChannelA.play(sndDa)
                        if integerValue & 2:
                            soundChannelB.play(sndDb)
                        if integerValue & 4:
                            soundChannelC.play(sndDc)
                        if integerValue & 8:
                            soundChannelD.play(sndDd)
                        if integerValue & 16:
                            soundChannelE.play(sndDe)
                        if integerValue & 32:
                            soundChannelF.play(sndDf)
                oldvalue = integerValue;
				
def Metronome(*args):
    while True:
        time.sleep(0.6)
        soundChannelG.play(sndMet)
	
	
#protocol example
#ProtHandle = protocol()
#senddata = [0,0,255,100,0,0,255,100,0,0,255,100,0,0,255,100,0,0,255,100]
#ProtHandle.transmit(10, senddata)

ProtHandle = protocol()

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()
pygame.init()
soundChannelA = pygame.mixer.Channel(1)
soundChannelB = pygame.mixer.Channel(2)
soundChannelC = pygame.mixer.Channel(3)
soundChannelD = pygame.mixer.Channel(4)
soundChannelE = pygame.mixer.Channel(5)
soundChannelF = pygame.mixer.Channel(6)
soundChannelG = pygame.mixer.Channel(7)

sndPa = pygame.mixer.Sound("sounds/piano/a.wav")
sndPb = pygame.mixer.Sound("sounds/piano/b.wav")
sndPc = pygame.mixer.Sound("sounds/piano/c.wav")
sndPd = pygame.mixer.Sound("sounds/piano/d.wav")
sndPe = pygame.mixer.Sound("sounds/piano/e.wav")
sndPf = pygame.mixer.Sound("sounds/piano/f.wav")
sndDa = pygame.mixer.Sound("sounds/drums/Bongo.wav")
sndDb = pygame.mixer.Sound("sounds/drums/Snare.wav")
sndDc = pygame.mixer.Sound("sounds/drums/Kick.wav")
sndDd = pygame.mixer.Sound("sounds/drums/Tom.wav")
sndDe = pygame.mixer.Sound("sounds/drums/Clap.wav")
sndDf = pygame.mixer.Sound("sounds/drums/Crash.wav")
sndMet = pygame.mixer.Sound("sounds/metronome.wav")

threading.Thread(target=MusicFunction).start() 
threading.Thread(target=Metronome).start() 

