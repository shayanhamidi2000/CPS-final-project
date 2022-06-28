from subprocess import call
import bluetooth as bt
import serial as ser
from serial.tools import list_ports
import time
from multiprocessing import Process, Queue


class DeviceNotFoundException(Exception):
    def __init__(self, device_name):
        self.device_name = device_name

    def what(self):
        return f"Bluetooth device named {self.device_name} could not be found!"

class CannotPairDeviceException(Exception):
    def __init__(self, device_name):
        self.device_name = device_name

    def what(self):
        return f"Bluetooth device named {self.device_name} could not be cannot be paired!"

class CannotFindPort(Exception):
    def __init__(self, device_name):
        self.device_name = device_name

    def what(self):
        return f"The port for bluetooth device named {self.device_name} could not be found!"

class BT:
    def __init__(self, bt_ecg_name):
        self.bt_ecg_name = bt_ecg_name
        self.bt_ecg_mac = None
        self.serial_port = None
    
    def connect_to_edge(self, scan_timeout=8):
        self.bt_ecg_mac = self.discover_devices(scan_timeout= scan_timeout)
        print(f'Successfully found device {self.bt_ecg_name} with mac address {self.bt_ecg_mac}')
        self.pair_device()
        time.sleep(4) #waiting for complete pairing
        print('Device is paired!')
        self.serial_port = ser.Serial(self.find_comport(), 115200, timeout=1)
        print(f'Successfully established the serial port!')
    
    def discover_devices(self, scan_timeout):
        devices = bt.discover_devices(lookup_names=True, duration=scan_timeout)
        for addr, name in devices:
            if name == self.bt_ecg_name:
                return addr
        raise DeviceNotFoundException(self.bt_ecg_name)

    def pair_device(self):
        if call(f'btpair -n\"{self.bt_ecg_name}\" -p', shell=True) != 0:
            raise CannotPairDeviceException(self.bt_ecg_name)

    def get_response_from_port(self, ser_port):
        response = ""
        for byte_num in range(18):
            data = ser_port.read()
            response = response + data.decode()
        return response

    def get_next_data_from_sensor(self):
        next_data = ""
        state_data_started = False
        while True:
            byte = self.serial_port.read().decode()
            if byte == '#':
                if state_data_started:
                    return int(next_data)
                else:
                    state_data_started = True
            elif state_data_started:
                next_data = next_data + byte
        

    def is_port_for_our_device(self, portInfo):
        ser_port = ser.Serial(portInfo.name, 115200, timeout=1)
        ser_port.write('start#'.encode())
        response = self.get_response_from_port(ser_port)
        ser_port.close()
        if response == self.bt_ecg_mac:
            return True
        return False

    def find_comport(self):
        ports_matched = list_ports.grep('Standard Serial over Bluetooth link*')
        for port in ports_matched:
            if self.is_port_for_our_device(port):
                return port.name
        raise CannotFindPort(self.bt_ecg_name)
