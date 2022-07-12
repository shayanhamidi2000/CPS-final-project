import sys
from bt import *
from plotter import *

if (len(sys.argv) != 2):
    print("One argument must be provided that is the edge device bluetooth name!")
    exit()
bt = BT(sys.argv[1])
try:
    bt.connect_to_edge()
except DeviceNotFoundException as exp:
    print(exp.what())
    exit()
except CannotPairDeviceException as exp:
    print(exp.what())
    exit()
except CannotFindPort as exp:
    print(exp.what())
    exit()

Plotter = plotter(window_size = 100, figsize=(10, 10))
for i in range(100000):
    Plotter.add_point(bt.get_next_data_from_sensor())

