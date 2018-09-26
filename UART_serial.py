from time import sleep
import serial, time, pygame, os
from subprocess import call


class Serial(object):

    def __init__(self):
        ##Initialize the serial port object for read and writes##
        ser = serial.Serial()
        ser.port = "/dev/ttyAMA0"
        ser.baudrate = 9600
        ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        ser.parity = serial.PARITY_NONE #set parity check: no parity
        ser.stopbits = serial.STOPBITS_ONE #number of stop bits
        #ser.timeout = None          #block read
        ser.timeout = 1            #non-block read
        #ser.timeout = 2              #timeout block read
        ser.xonxoff = False     #disable software flow control
        ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        ser.writeTimeout = 2     #timeout for write

        try: 
            ser.open()
        except Exception, e:
            print "error open serial port: " + str(e)
            exit()

        if ser.isOpen():
            try:
                ser.flushInput() #flush input buffer, discarding all its contents
                ser.flushOutput()#flush output buffer, aborting current output 
                                 #and discard all that is in buffer
                ser.close()
            except Exception, e1:
                print "error communicating...: " + str(e1)
                
        else:
            print "cannot open serial port "

        # Assign ser to self.ser for future usage. Done to avoid confusion using self.
        self.ser = ser

    def Read_data(self):
        data_byte = 0
        data_length = 5
        data_in = [data_length]
        if self.ser.isOpen():
            try:
                for data_byte in range(data_length):
                    data_in[data_byte] = self.ser.readline()
                return [data_in]
                self.ser.close()
            except Exception, e2:
                print "error reading data...: " + str(e2)
                

    def Write_data(self, data):
        data_out = []
        data_line = 0
        if self.ser.isOpen():
            try:
                for data_line in range(data_out):
                    data_out[data_line] = self.ser.readline()
                self.ser.close()
            except Exception, e3:
                print "error sending data...: " + str(e3)            




########################################   MAIN    ######################################## 
if __name__ == '__main__':

    #create serial class object tp acces the serial port
    serobj = Serial()



