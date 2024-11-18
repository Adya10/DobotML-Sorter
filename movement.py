from serial.tools import list_ports
from pydobotplus import Dobot
import time

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[3].device

device = Dobot(port=port)

#to calibrate the device to home position
device.home()

device.clear_alarms()

#False is open and True is close for gripper
device.grip(False)

#posotion of conveyor belt
device.move_to(x=-4.214, y=-268.311, z=32.32,r=-83.84)
device.grip(True) #grab the cube
time.sleep(3)

#positon of red
device.move_to(x=-48.22, y=205.04, z=-7.601,r=110.295)
device.grip(False) #drop the cube
time.sleep(3)

#back to coveyor
device.grip(True)
device.move_to(x=-4.214, y=-268.311, z=32.32,r=-83.84)
device.grip(True) #grab the cube
time.sleep(3)

#position of green
device.move_to(x=50.122, y=210.488, z=-11.09,r=83.5)
device.grip(False)
time.sleep(3)

#back to coveyor
device.grip(True)
device.move_to(x=-4.214, y=-268.311, z=32.32,r=-83.84)
device.grip(True) #grab the cube
time.sleep(3)

#position of blue
device.move_to(x=157.03, y=178.622, z=-13.79,r=55.73)
device.grip(False)
time.sleep(3)

#back to coveyor
device.grip(True)
device.move_to(x=-4.214, y=-268.311, z=32.32,r=-83.84)
device.grip(True) #grab the cube
time.sleep(3)


device.close()
