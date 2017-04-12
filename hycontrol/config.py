
import yaml

class VFDConf:

    def __init__(self, port= '/dev/ttyUSB0', rate=9600, address=1, timeout=1):
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

    def __init__(self, address, unit='', unit_scale='', description='', short='', **kwargs):
        self.address = address
        self.scale = unit_scale
        self.unit = unit
        self.description = description
        self.shortdesc = short
        self.value = None

    def __str__(self):
        return """PD{0:03d}: {1} unit: {2} scale: {3}
    {3}\n""".format(self.address, self.shortdesc, self.description, self.unit, self.scale)

class RegisterMap:

    def __init__(self, mapfile):
        self.m = {}
        with open(mapfile, 'r') as f:
            rawdata = yaml.load(f, Loader=yaml.CLoader)
            for addr, reg in rawdata.items():
                self.m[addr] = Register(addr, **reg)

    def reg(self, addr):
        return self.m[addr]
