import time
from time import sleep
import serial
import pygame
import os
from subprocess import call


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.mixer.init()
    sndA = pygame.mixer.Sound("sounds/A_Triplet_Riff_2a.wav")
    sndB = pygame.mixer.Sound("sounds/piano/e.wav")
    soundChannelA = pygame.mixer.Channel(1)
    soundChannelB = pygame.mixer.Channel(2)
    #call("sudo amixer cset numid=3 1", shell=True)
    
    ser = serial.Serial(
        port='COM7',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1)

    while True:
        sensor_input = ser.readline()

        ##print sensor_input
        if ("button_1" in sensor_input):
            print("Playing sound 1")
            soundChannelA.play(sndA)
            #return [music.play appropriate sound]
            ##pygame.mixer.music.load("sounds/piano/a.wav")
            ##pygame.mixer.music.play()
            ser.write(str("Ack_button_1"))
        elif ("button_2" in sensor_input):
            #return [music.play appropriate sound]
            ser.write("Ack_button_2")
            soundChannelB.play(sndB)
