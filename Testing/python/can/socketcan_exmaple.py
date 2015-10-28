import struct 
import socket 
import string 

def dump(s): 
    return ' '.join(["%02X" % ord(x) for x in s]) 

# return tuple (id, dlc, data) 
def unpack_can_frame(can_frame): 
    # attention: 'data' is 8-byte-aligned 
    id, dlca, data = struct.unpack("I4s8s", can_frame) 
    dlc = ord(dlca[0]) 
    return id, dlc, data[:dlc] 

# pretty print can_frame struct 
def dump_can_frame(can_frame): 
    id, dlc, data = unpack_can_frame(can_frame) 
    print "id:%08x, dlc:%d, data:%s" % (id, dlc, dump(data)) 

# pretty print can_frame struct in the socketcan way 
def dump_can_frame_sc(can_frame): 
    id, dlc, data = unpack_can_frame(can_frame) 

    s_data = ''.join(["%02X" % ord(x) for x in data]) 
    if (id & socket.CAN_RTR_FLAG): 
        s_data = "R" 
        id = id & ~socket.CAN_RTR_FLAG 

    if (id & socket.CAN_EFF_FLAG): 
        id = id & ~socket.CAN_EFF_FLAG 
        print "%08x#%s" % (id, s_data) 
    else: 
        print "%03x#%s" % (id, s_data) 

# build packed can_frame struct from id, dlc and data 
def build_can_frame(id, dlc, data): 
    fill = "\0\0\0\0\0\0\0\0" 
    dlca = chr(dlc) + "\0\0\0" 
    x = struct.pack("i4s%ds%ds" % (dlc, 8 - dlc), 
                    id, dlca, data[:dlc], fill[:8-dlc]) 
    return x 

# build packed can_frame struct from socketcan text representation 
def build_can_frame_sc(text): 
    s_id, s_data = string.split(text, '#') 
    id = int(s_id, 16) 

    if (len(s_data) == 1) and (s_data[0] == "R"): 
        id |= socket.CAN_RTR_FLAG; 
    if len(s_id) == 8: 
        id |= socket.CAN_EFF_FLAG; 
    dlc = len(s_data) >> 1 
    data = ''.join(["%c" % int(s_data[x*2:(x+1)*2],16) for x in range(dlc)]) 
    return build_can_frame(id, dlc, data) 


if __name__=='__main__': 
    # create CAN socket 
    s = socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW) 

    # setup id filter 
    id = 0 
    mask = 0 
    s.setsockopt(socket.SOL_CAN_RAW, socket.CAN_RAW_FILTER, 
                 struct.pack("II", id, mask)) 

    # enable/disable loopback 
    loopback = 0 
    s.setsockopt(socket.SOL_CAN_RAW, socket.CAN_RAW_LOOPBACK, 
                 struct.pack("I", loopback)) 

    # bind to interface "canX" or "any") 
    # tuple is (interface, reserved(can_addr)) 
    s.bind(("can0",)) 

    while 1: 
        cf, addr = s.recvfrom(16) 
        print addr 
        dump_can_frame(cf) 
        dump_can_frame_sc(cf) 

        # send echo 
        try: 
            s.send(cf) 
        except socket.error: 
            print "Error sending CAN frame" 

        # test 1 
        try: 
            cf = build_can_frame(0, 8, "\x11\x22\x33\x44\x55\x66\x77\x88") 
            dump_can_frame(cf) 
            dump_can_frame_sc(cf) 
            s.send(cf) 
        except socket.error: 
            print "Error sending CAN frame" 

        # test 2 
        try: 
            cf = build_can_frame_sc("12345678#11223344556677") 
            dump_can_frame(cf) 
            dump_can_frame_sc(cf) 
            s.send(cf) 
        except socket.error: 
            print "Error sending CAN frame" 

        # test 2 
        try: 
            cf = build_can_frame_sc("123#12345678") 
            dump_can_frame(cf) 
            dump_can_frame_sc(cf) 
            s.send(cf) 
        except socket.error: 
            print "Error sending CAN frame" 