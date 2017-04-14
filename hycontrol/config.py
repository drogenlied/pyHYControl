
import yaml

class VFDConf:

    def __init__(self, port='/dev/ttyUSB0', rate=9600, address=1, timeout=1):
        self.port = port
        self.rate = rate
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


control_status = {
    0: 'run',
    1: 'jog',
    2: 'reserved',
    3: 'running',
    4: 'jogging',
    5: 'reserved',
    6: 'braking',
    7: 'track start',
    8: '?',
    9: '?'
    }

control_commands = {
    0: 'run',
    1: 'forward',
    2: 'reverse',
    3: 'stop',
    4: 'reserved',
    5: 'jog',
    6: 'jogf',
    7: 'jogr',
    }

control_values = {
    0: {
        'name': 'set frequency',
        'unit': 'Hz',
        'scale': 0.01 },
    1: {
        'name': 'output frequency',
        'unit': 'Hz',
        'scale': 0.01 },
    2: {
        'name': 'output current',
        'unit': 'A',
        'scale': 1 },
    3: {
        'name': 'rott',
        'unit': 'rpm',
        'scale': 1 },
    4: {
        'name': 'DC voltage',
        'unit': 'V',
        'scale': 0.1 },
    5: {
        'name': 'AC voltage',
        'unit': 'V',
        'scale': 0.1 },
    6: {
        'name': 'cont',
        'unit': 'A',
        'scale': 1 },
    7: {
        'name': 'tmp',
        'unit': 'C',
        'scale': 1 }
}

