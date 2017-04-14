
import os

from .device import *
from .config import *

if __name__ == '__main__':
    c = VFDConf(timeout=0.1)
    r = RegisterMap(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'registers.yml'))
    d = VFDDevice(c, r)
    d.connect()

    d.loop_test([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    #d.write_function_data(1, 0)
    #d.read_function_data(1)
    for i in range(200):
        if not d.is_parameter_reserved(i):
            d.read_function_data(i)

