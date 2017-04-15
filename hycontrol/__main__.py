
import os
import time
import argparse

from .device import *
from .config import *

def test(d):
    #d.loop_test([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    #d.write_function_data(1, 2)
    #d.write_function_data(2, 2)

    time.sleep(2)
    d.write_control_data(1)
    d.write_control_data(0)
    d.write_freq(400)

    for t in range(15):
        time.sleep(2)
        print([d.read_control_data(i) for i in range(6)])

    d.write_freq(0)
    for t in range(15):
        time.sleep(2)
        print([d.read_control_data(i) for i in range(6)])

    d.write_control_data(3)

    #d.write_function_data(1, 0)
    #d.write_function_data(2, 0)

    #d.write_function_data(1, 0)
    #d.read_function_data(1)

    #for i in range(200):
    #    if not d.is_parameter_reserved(i):
    #        d.read_function_data(i)

def read_parameter(device, args):
    device.read_function_data(args.parameter)

def write_parameter(device, args):
    device.write_function_data(args.parameter, args.value)

def write_command(device, args):
    cc = control_commands
    cmd = list(cc.keys())[list(cc.values()).index(args.command)]
    device.write_control_data(cmd)

def read_status(device, args):
    cv = control_values
    cmd = [k for k, v in cv.items() if v['short'] == args.indicator][0]
    ret = device.read_control_data(cmd)
    print('{}: {:.2f} {}'.format(cv[cmd]['short'], ret[0], ret[1]))

def write_frequency(device, args):
    device.write_freq(args.frequency)

def loopback_test(device, args):
    return 0 if device.loop_test(list(args.data.encode('ascii'))) else -1

if __name__ == '__main__':

    p = argparse.ArgumentParser('hycontrol', description='Interact with a Huanyang VFD.')
    p.add_argument('-d', '--device', default='/dev/ttyUSB0', help='Serial device')
    p.add_argument('-b', '--baudrate', type=int,
        choices=[4800, 9600, 19200, 38400], default=9600, help='Baud rate of connection')
    p.add_argument('-p', '--parity', default='N', choices=['N', 'E', 'O'], help='No / Odd / Even parity bit')
    p.add_argument('-a', '--address', type=int, default=1, help='Target device address')
    p.add_argument('-t', '--timeout', type=float, default=0.1, help='Read timeout in seconds')
    p.add_argument('--verbose', '-v', action='count', help='each instance gives more debug output')

    sub = p.add_subparsers(title='Subcommands')

    rp = sub.add_parser('read', aliases=['r'], help='Read parameter from VFD.')
    rp.add_argument('parameter', type=int, help='VFD parameter to be read')
    rp.set_defaults(function=read_parameter)

    wp = sub.add_parser('write', aliases=['w'], help='Write value to parameter.')
    wp.add_argument('parameter', type=int, help='VFD parameter to be written')
    wp.add_argument('value', type=float, help='value to be written to parameter')
    wp.set_defaults(function=write_parameter)

    cp = sub.add_parser('command', aliases=['c', 'cmd'], help='Send command to VFD.')
    cp.add_argument('command', choices=control_commands.values(), help='Command to be sent to VFD')
    cp.set_defaults(function=write_command)

    sp = sub.add_parser('status', aliases=['s', 'stat'], help='Get status indicator from VFD.')
    sp.add_argument('indicator',
        choices=[v['short'] for k, v in control_values.items()],
        help='Status indicator to be read from VFD.')
    sp.set_defaults(function=read_status)

    fp = sub.add_parser('frequency', aliases=['f', 'freq'], help='Set output frequency.')
    fp.add_argument('frequency', type=float, help='Motor target frequency.')
    fp.set_defaults(function=write_frequency)

    lp = sub.add_parser('loopback', aliases=['l', 'loop'], help='Do a loopback communication test with the VFD.')
    lp.add_argument('data', help='Loopback data for testing.')
    lp.set_defaults(function=loopback_test)

    args = p.parse_args()
    #print(args)

    conf = VFDConf(
        port=args.device,
        rate=args.baudrate,
        parity=args.parity,
        address=args.address,
        timeout=args.timeout)

    regmap = RegisterMap(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), 'registers.yml'))

    d = VFDDevice(conf, regmap)

    d.connect()
    args.function(d, args)
    d.close()
