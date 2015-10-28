import can

can_interface = 'can0'
bus = can.interface.Bus(can_interface, bustype='socketcan')
message = bus.recv(1.0)  # Timeout in seconds.

if message is None:
    print('Timeout occurred, no message.')