from time import sleep
import serial, time, pygame, os
from subprocess import call


########################################   Serial Init    ########################################           
##def Serial_Init():
##    #initialization and open the port
##    #possible timeout values:
##    #    1. None: wait forever, block call
##    #    2. 0: non-blocking mode, return immediately
##    #    3. x, x is bigger than 0, float allowed, timeout block call
##
##    ser = serial.Serial()
##    ser.port = "/dev/ttyAMA0"
##    ser.baudrate = 9600
##    ser.bytesize = serial.EIGHTBITS #number of bits per bytes
##    ser.parity = serial.PARITY_NONE #set parity check: no parity
##    ser.stopbits = serial.STOPBITS_ONE #number of stop bits
##    #ser.timeout = None          #block read
##    ser.timeout = 1            #non-block read
##    #ser.timeout = 2              #timeout block read
##    ser.xonxoff = False     #disable software flow control
##    ser.rtscts = False     #disable hardware (RTS/CTS) flow control
##    ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
##    ser.writeTimeout = 2     #timeout for write
##    
##    try: 
##        ser.open()
##        print (ser)
##    except Exception, e:
##        print "error open serial port: " + str(e)
##        exit()
##
##    if ser.isOpen():
##        try:
##            ser.flushInput() #flush input buffer, discarding all its contents
##            ser.flushOutput()#flush output buffer, aborting current output 
##                             #and discard all that is in buffer
##            ser.close()
##        except Exception, e1:
##            print "error communicating...: " + str(e1)
##            
##    else:
##        print "cannot open serial port "



########################################   sound init    ######################################## 
def Sound_Init():
    pygame.init()
    pygame.mixer.init(48000, -16, 1, 1024)


    #moet nog recursief!!
    
    sndA = pygame.mixer.Sound("sounds/piano/a.wav")
    sndB = pygame.mixer.Sound("sounds/piano/b.wav")
    sndC = pygame.mixer.Sound("sounds/piano/c.wav")
    sndD = pygame.mixer.Sound("sounds/piano/d.wav")
    sndE = pygame.mixer.Sound("sounds/piano/e.wav")
    
    soundChannelA = pygame.mixer.Channel(1)
    soundChannelB = pygame.mixer.Channel(2)
    soundChannelC = pygame.mixer.Channel(3)
    soundChannelD = pygame.mixer.Channel(4)
    soundChannelE = pygame.mixer.Channel(5)

    #set audio output to aux out instead of hdmi audio out
    call("sudo amixer cset numid=3 1", shell=True)



########################################   uart Get  ######################################## 
def UART_get():
    if ser.isOpen():
        try:
            data = ser.readline()   #read one data byte 
            return data
            ser.flushInput()        #clear input buffer
        except Exception, e2:
            print "error reading data...: " + str(e2)


                    
########################################   uart Send  ######################################## 
def UART_send(data):
    if ser.isOpen():
        try:
            ser.write(data)         #write one data byte 
            ser.flushOutput()       #clear output buffer
            ser.close()
        except Exception, e3:
            print "error sending data...: " + str(e3)

            

########################################   play sounds  ########################################
def play_sounds():
    if ("button_1" in sensor_input):
        soundChannelA.play(sndA)
        ser.write(str("Ack_button_1"))
    elif ("button_2" in sensor_input):
        ser.write("Ack_button_2")
        soundChannelB.play(sndB)

########################################   MAIN  ##############################################


if __name__ == '__main__':

    ser = serial.Serial(
    port = "/dev/ttyAMA0",
    baudrate = 9600,
    bytesize = serial.EIGHTBITS,     #number of bits per bytes
    parity = serial.PARITY_NONE,     #set parity check: no parity
    stopbits = serial.STOPBITS_ONE,  #number of stop bits
    #timeout = None,                 #block read
    timeout = 1)#,                     #non-block read
    #timeout = 2,                    #timeout block read
    #xonxoff = False,                 #disable software flow control
    #rtscts = False,                  #disable hardware (RTS/CTS) flow control
    #dsrdtr = False,                  #disable hardware (DSR/DTR) flow control
    #writeTimeout = 2)                #timeout for write
    
    while True:
        response = UART_get()
        print response
        #ser.write(bytes(0x55))
        
        
