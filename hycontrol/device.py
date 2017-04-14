
import crcmod
import struct
import serial
from .config import control_commands, control_status, control_values

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
        if int(message[1]) & 0xF0 > 0:
            print('Execution error:', hex(int(message[1])))
        dlen = message[2]
        data = message[3:-2]
        return int(dlen) == len(data)
    else:
        return False

def print_msg_error(message):
    print('Comm error:')
    print(message)
    print('calc_crc:', hy_crc(message[:-2]), 'sent_crc:', list(message[-2:]))
    print('data_length:', len(message[3:-2]), 'sent_length:', int(message[2]))

class VFDDevice:

    def __init__(self, config, regmap):
        self.config = config
        self.conn = None
        self.m = regmap

    def connect(self):
        self.conn = serial.Serial(
            port=self.config.port,
            baudrate=self.config.rate,
            timeout=self.config.timeout)

    def is_parameter_reserved(self, parameter):
        return 'reserved' in self.m.reg(parameter).unit

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

    def read_function_data(self, parameter):
        packet = self.build_packet(0x01, [parameter])
        self.conn.write(bytes(packet))
        ans = self.conn.read(8)
        if check_msg(ans):
            data = ans[3:-2]
            param = data[0]
            value = int.from_bytes(bytes(data[1:]), byteorder='big')
            print('read:', self.m.reg(parameter).format_value(value))
            ret = value * self.m.reg(parameter).scale, self.m.reg(parameter).unit
        else:
            print_msg_error(ans)
            ret = -1, 'Error'
        return ret

    def write_function_data(self, parameter, data):
        pdata = [parameter]
        if data == 0:
            pdata.append(0)
        else:
            pdata.extend(
                list(data.to_bytes((data.bit_length() + 7) // 8, 'big')))
        packet = self.build_packet(0x02, pdata)
        self.conn.write(bytes(packet))
        ans = self.conn.read(8)
        if check_msg(ans):
            rdata = ans[3:-2]
            param = rdata[0]
            value = int.from_bytes(bytes(rdata[1:]), byteorder='big')
            print('written:', self.m.reg(parameter).format_value(value))
            ret = value * self.m.reg(parameter).scale, self.m.reg(parameter).unit
        else:
            print_msg_error(ans)
            ret = -1, 'Error'
        return ret

    def write_control_data(self, data):
        packet = self.build_packet(0x03, [data])
        self.conn.write(bytes(packet))
        ans = self.conn.read(6)
        if check_msg(ans):
            rdata = ans[3:-2]
            value = int.from_bytes(bytes(rdata), byteorder='big')
            print('Command:', control_commands[int(data)])
            print('Status:', control_status[value])
            ret = value
        else:
            print_msg_error(ans)
            ret = -1
        return ret

    def read_control_data(self, parameter):
        packet = self.build_packet(0x04, [parameter])
        self.conn.write(bytes(packet))
        ans = self.conn.read(8)
        if check_msg(ans):
            rdata = ans[3:-2]
            value = int.from_bytes(bytes(rdata[1:]), byteorder='big')
            cval = control_values[int(parameter)]
            #print(
            #    cval['name'],
            #    value * cval['scale'],
            #    cval['unit'])
            ret = value * cval['scale'], cval['unit']
        else:
            print_msg_error(ans)
            ret = -1, "Error"
        return ret

    def write_freq(self, freq):
        pdata = []
        if freq == 0:
            pdata.extend([0, 0])
        else:
            pdata.extend(
                list((freq * 100).to_bytes(2, 'big')))

        packet = self.build_packet(0x05, pdata)
        self.conn.write(bytes(packet))
        ans = self.conn.read(8)
        if check_msg(ans):
            rdata = ans[3:-2]
            value = int.from_bytes(bytes(rdata), byteorder='big')
            print('Set frequency command:', value/100)
            ret = value/100
        else:
            print_msg_error(ans)
            ret = -1
        return ret

    def loop_test(self, data):
        packet = self.build_packet(0x08, data)
        self.conn.write(bytes(packet))
        ans = self.conn.read(len(packet))
        if check_msg(ans):
            data = ans[3:-2]
            param = data[0]
            print(list(data))
            ret = True
        else:
            print_msg_error(ans)
            ret = False
        return ret

    def print_status(self):
        for i in range(8):
            self.read_control_data(i)
