from serial.tools import list_ports

import pydobotplus

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[3].device

device = pydobotplus.Dobot(port=port)

device.clear_alarms()

device.grip(False)

device._set_end_effector_gripper(enable=False)


device.close()
