
import crcmod
import struct

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

def build_packet(addr, function, data):
    packet = []
    packet.append(addr)
    packet.append(function)
    packet.append(len(data))
    packet.extend(data)
    crc = hy_crc(packet)
    packet.extend(crc)

    #print('BUILD:', packet)
    return packet

def read_fc_data(conn, addr, parameter):
    packet = build_packet(addr, 0x01, [parameter])
    conn.write(bytes(packet))
    ans = conn.read(8)
    if check_msg(ans):
        data = ans[3:-2]
        param = data[0]
        value = int.from_bytes(bytes(data[1:]), byteorder='big')
        print('PD{0:03d}: {1}'.format(param, value))

def write_fc_data(conn, addr, data):
    packet = build_packet(addr, 0x02, data)
    conn.write(bytes(packet))
    ans = conn.read(8)
    if check_msg(ans):
        print(data)

def write_control_data(conn, addr, data):
    packet = build_packet(addr, 0x03, data)
    conn.write(bytes(packet))
    ans = conn.read(6)
    if check_msg(ans):
        print()

def read_control_data(conn, addr, data):
    packet = build_packet(addr, 0x04, data)
    conn.write(bytes(packet))
    ans = conn.read(8)
    if check_msg(ans):
        print(data)

def write_freq(conn, addr, data):
    packet = build_packet(addr, 0x05, data)
    conn.write(bytes(packet))
    ans = conn.read(7)
    if check_msg(ans):
        print(data)

#def loop_test(conn, addr, data):
