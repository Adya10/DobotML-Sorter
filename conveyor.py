from serial.tools import list_ports
from pydobotplus import Dobot, CustomPosition

available_ports = list_ports.comports()
print(f'available ports: {[x.device for x in available_ports]}')
port = available_ports[3].device

device = Dobot(port=port)

# Create a custom position
pos1 = CustomPosition(x=200, y=50, z=50)

# Move using direct coordinates
device.move_to(x=200, y=50, z=50)

# Move using custom position
device.move_to(position=pos1)

# Control the conveyor belt
def once():
    device.conveyor_belt(speed=0.5, direction=1)
    device.conveyor_belt_distance(speed_mm_per_sec=100, distance_mm=200, direction=1)
    print(device.get_ir(port=1))


def inf():
    while True:
        device.conveyor_belt(speed=0.5, direction=1)
        device.conveyor_belt_distance(speed_mm_per_sec=100, distance_mm=200, direction=1)
        print(device.get_ir(port=2))

once()
# inf()

device.close()

