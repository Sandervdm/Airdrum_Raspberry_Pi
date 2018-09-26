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
    data_type = 0
    data_array = []

    def __init__(self):
        # Initialise the serial connection
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
            # Create checksum
            check = 85 + type + len(data)
            # Fill array with data
            send_array = []
            # preamble
            send_array += chr(85)
            # Data length
            send_array += chr(len(data))
            # Data type
            send_array += chr(type)
            for d in data:
                send_array += chr(d)
                check += d
            check = ~check
            send_array += chr(check % 0xFF)
            # Sent data
            self.ser.write(send_array)
            return True
        else:
            return False

    def receive(self):
        try:
            # Empty data array
            del self.dataarray[:]
            # Check if startbyte is received
            start_byte = self.ser.read()
            if ord(start_byte) == 85:
                # Read data length
                length = ord(self.ser.read())
                # Read data type
                self.data_type = ord(self.ser.read())
                # Read all data
                for i in range(0, length):
                    self.data_array += self.ser.read()
                # Read checksum
                check = ord(self.ser.read())
                return True
            else:
                return False
        except Exception as eee:
            return False
            #print("Receiving gave an error" + str(eee))

    def close(self):
        self.ser.close()
		

data_array_last = [0, 0, 0, 0, 0, 0]
data_array = [0, 0, 0, 0, 0, 0]

def prot_to_hand_data(panel, trigger):
    print str(panel)+" "+str(trigger)
    if data_array[panel] > trigger:
        if data_array_last[panel] > trigger:
            data_array_last[panel] = data_array[panel]
            return 0
        if data_array_last[panel] <= trigger:
            data_array_last[panel] = data_array[panel]
            return 1
    if data_array[panel] <= trigger:
        if data_array_last[panel] > trigger:
            data_array_last[panel] = data_array[panel]
            return -1
        if data_array_last[panel] <= trigger:
            data_array_last[panel] = data_array[panel]
            return 0

		
def MusicFunction(*args):
	while True:
	    if ProtHandle.receive():
            if ProtHandle.datatype == 11:
                # Read data
                data_array[0] = ProtHandle.dataarray[0]
                data_array[1] = ProtHandle.dataarray[1]
                data_array[2] = ProtHandle.dataarray[2]
                data_array[3] = ProtHandle.dataarray[3]
                data_array[4] = ProtHandle.dataarray[4]
                data_array[5] = ProtHandle.dataarray[5]
                # check data and play or stop sounds per panel
                val = prot_to_hand_data(0, 100)
                if val == 1:
                    soundChannelA.play(sndPa)
                if val == -1:
                    soundChannelA.stop(sndPa)
                val = prot_to_hand_data(1, 100)
                if val == 1:
                    soundChannelB.play(sndPb)
                if val == -1:
                    soundChannelB.stop(sndPb)
                val = prot_to_hand_data(2, 100)
                if val == 1:
                    soundChannelC.play(sndPc)
                if val == -1:
                    soundChannelC.stop(sndPc)
                val = prot_to_hand_data(3, 100)
                if val == 1:
                    soundChannelD.play(sndPd)
                if val == -1:
                    soundChannelD.stop(sndPd)
                val = prot_to_hand_data(4, 100)
                if val == 1:
                    soundChannelE.play(sndPe)
                if val == -1:
                    soundChannelE.stop(sndPe)
                val = prot_to_hand_data(5, 100)
                if val == 1:
                    soundChannelF.play(sndPf)
                if val == -1:
                    soundChannelF.stop(sndPf)

				
def Metronome(*args):
    while True:
        time.sleep(0.6)
        soundChannelG.play(sndMet)
	


# get protocol handle
ProtHandle = protocol()
# initialization data for leds
led_color_data = [0,0,255,100,0,0,255,100,0,0,255,100,0,0,255,100,0,0,255,100]
ProtHandle.transmit(10, led_color_data)

# init pygame mixer
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.mixer.init()
pygame.init()

# create channels
soundChannelA = pygame.mixer.Channel(1)
soundChannelB = pygame.mixer.Channel(2)
soundChannelC = pygame.mixer.Channel(3)
soundChannelD = pygame.mixer.Channel(4)
soundChannelE = pygame.mixer.Channel(5)
soundChannelF = pygame.mixer.Channel(6)

# Create sound handles
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

