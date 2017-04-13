
import crcmod
import struct
import serial

crc16 = crcmod.predefined.mkPredefinedCrcFun('modbus')

def hy_crc(message):
    return list(struct.pack('<H', crc16(bytes(message))))

def check_crc(message):
    if len(message) > 5:
        calc_crc = hy_crc(message[:-2])
        msg_crc = list(message[-2:])
        #print('CRC', calc_crc, list(msg_crc))
        return calc_crc == msg_crc
    else:
        return False

def check_msg(message):
    if check_crc(message):
        dlen = message[2]
        data = message[3:-2]
        return int(dlen) == len(data)
    else:
        return False


class VFDDevice:

    def __init__(self, config, regmap):
        self.config = config
        self.m = regmap
        self.conn = None

    def connect(self):
        self.conn = serial.Serial(
            port=self.config.port,
            baudrate=self.config.rate,
            timeout=self.config.timeout)

    def build_packet(self, function, data):
        packet = []
        packet.append(self.config.address)
        packet.append(function)
        packet.append(len(data))
        packet.extend(data)
        crc = hy_crc(packet)
        packet.extend(crc)

        #print('BUILD:', packet)
        return packet

    def read_fc_data(self, parameter):
        packet = self.build_packet(0x01, [parameter])
        self.conn.write(bytes(packet))
        ans = self.conn.read(8)
        if check_msg(ans):
            data = ans[3:-2]
            param = data[0]
            value = int.from_bytes(bytes(data[1:]), byteorder='big')
            print(self.m.reg(parameter).format_value(value))

    def write_fc_data(self, parameter, data):
        packet = self.build_packet(0x02, data)
        self.conn.write(bytes(packet))
        ans = self.conn.read(8)
        if check_msg(ans):
            print(data)

    def write_control_data(self, parameter, data):
        packet = self.build_packet(0x03, data)
        self.conn.write(bytes(packet))
        ans = self.conn.read(6)
        if check_msg(ans):
            print()

    def read_control_data(self, parameter, data):
        packet = self.build_packet(0x04, data)
        self.conn.write(bytes(packet))
        ans = self.conn.read(8)
        if check_msg(ans):
            print(data)

    def write_freq(self, freq):
        packet = self.build_packet(0x05, freq)
        self.conn.write(bytes(packet))
        ans = self.conn.read(7)
        if check_msg(ans):
            print(ans)

    def loop_test(self, data):
        packet = self.build_packet(0x08, data)
        self.conn.write(bytes(packet))
        ans = self.conn.read(len(packet))
        if check_msg(ans):
            print(ans)
        else:
            print('Comm error: no checksum match')

