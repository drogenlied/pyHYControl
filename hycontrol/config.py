
import yaml

class VFDConf:

    def __init__(self, port='/dev/ttyUSB0', rate=9600, parity='N', address=1, timeout=1):
        self.port = port
        self.rate = rate
        self.parity = parity
        self.address = address
        self.timeout = timeout

    def load(self, configfile):
        with open(configfile, 'r') as f:
            rawcfg = yaml.load(f, Loader=yaml.CLoader)
            if 'com_port' in rawcfg:
                self.port = rawcfg['com_port']
            if 'baudrate' in rawcfg:
                self.rate = rawcfg['baudrate']
            if 'bus_address' in rawcfg:
                self.address = rawcfg['bus_address']
            if 'timeout' in rawcfg:
                self.timeout = rawcfg['timeout']

class Register:

    def __init__(self, address, unit='', scale='', description='', short='', **kwargs):
        self.address = address
        self.scale = scale
        self.unit = unit
        self.description = description
        self.shortdesc = short
        self.value = None

    def __str__(self):
        return """PD{0:03d}: {1} unit: {2} scale: {3}
    {3}\n""".format(self.address, self.shortdesc, self.description, self.unit, self.scale)

    def format_value(self, value):
        return 'PD{0:03d}: {1} {2}'.format(self.address, value * self.scale, self.unit)

class RegisterMap:

    def __init__(self, mapfile):
        self.m = {}
        with open(mapfile, 'r') as f:
            rawdata = yaml.load(f, Loader=yaml.CLoader)
            for addr, reg in rawdata.items():
                self.m[addr] = Register(addr, **reg)

    def reg(self, addr):
        return self.m[addr]


control_commands = {
    0x00: 'status',
    0x03: 'run_fwd',
    0x11: 'run_rev',
    0x08: 'stop'
}

control_bits = {
    0x01: 'run',
    0x02: 'forward',
    0x04: 'reverse',
    0x08: 'stop',
    0x10: 'reverse',
    0x20: 'jog',
    0x40: 'jogf',
    0x80: 'jogr',
    }

status_bits = {
    0x01: 'cmd_run',
    0x02: 'cmd_jog',
    0x04: 'cmd_reverse',
    0x08: 'running',
    0x10: 'jogging',
    0x20: 'run_reverse',
    0x40: 'braking',
    0x80: 'track start',
    }

control_values = {
    0: {
        'name': 'target frequency',
        'short': 'fset',
        'unit': 'Hz',
        'scale': 0.01 },
    1: {
        'name': 'output frequency',
        'short': 'fout',
        'unit': 'Hz',
        'scale': 0.01 },
    2: {
        'name': 'output current',
        'short': 'aout',
        'unit': 'A',
        'scale': 0.1 },
    3: {
        'name': 'rotations per minute',
        'short': 'rpm',
        'unit': 'rpm',
        'scale': 1 },
    4: {
        'name': 'DC voltage',
        'short': 'vdc',
        'unit': 'V',
        'scale': 0.1 },
    5: {
        'name': 'AC voltage',
        'short': 'vac',
        'unit': 'V',
        'scale': 0.1 },
    6: {
        'name': 'cont',
        'short': 'cont',
        'unit': 'h',
        'scale': 1 },
    7: {
        'name': 'Inverter temperature',
        'short': 'temp',
        'unit': 'C',
        'scale': 1 }
}

