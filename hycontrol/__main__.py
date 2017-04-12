
import serial
from .comm import *
from .config import *

if __name__ == '__main__':
    c = VFDConf()
    s = serial.Serial(port=c.port, baudrate=c.rate, timeout=c.timeout)

    read_fc_data(s, c.address, 0)
    read_fc_data(s, c.address, 1)
    read_fc_data(s, c.address, 2)
    read_fc_data(s, c.address, 3)
    read_fc_data(s, c.address, 4)
    read_fc_data(s, c.address, 5)
    read_fc_data(s, c.address, 6)
    read_fc_data(s, c.address, 7)
    read_fc_data(s, c.address, 8)
    read_fc_data(s, c.address, 9)
    read_fc_data(s, c.address, 10)
    read_fc_data(s, c.address, 11)
    #read_fc_data(s, c.address, 12)
    read_fc_data(s, c.address, 13)
    read_fc_data(s, c.address, 14)
    read_fc_data(s, c.address, 15)
    read_fc_data(s, c.address, 16)
    read_fc_data(s, c.address, 17)
    read_fc_data(s, c.address, 18)
    read_fc_data(s, c.address, 19)
    read_fc_data(s, c.address, 20)
    read_fc_data(s, c.address, 21)
    #read_fc_data(s, c.address, 22)
    read_fc_data(s, c.address, 23)
    read_fc_data(s, c.address, 24)

    read_fc_data(s, c.address, 141)
    read_fc_data(s, c.address, 142)
    read_fc_data(s, c.address, 143)
    read_fc_data(s, c.address, 144)

    read_fc_data(s, c.address, 163)
    read_fc_data(s, c.address, 164)
    read_fc_data(s, c.address, 165)

    read_fc_data(s, c.address, 173)
    read_fc_data(s, c.address, 174)
    read_fc_data(s, c.address, 175)
    read_fc_data(s, c.address, 176)
    read_fc_data(s, c.address, 177)
    read_fc_data(s, c.address, 178)
    read_fc_data(s, c.address, 179)
    read_fc_data(s, c.address, 180)
    read_fc_data(s, c.address, 181)
    read_fc_data(s, c.address, 182)
    read_fc_data(s, c.address, 183)

