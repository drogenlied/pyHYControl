
import os

from .device import *
from .config import *

if __name__ == '__main__':
    c = VFDConf()
    r = RegisterMap(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'registers.yml'))
    d = VFDDevice(c, r)
    d.connect()

    for i in range(40):
        d.read_fc_data(i)

