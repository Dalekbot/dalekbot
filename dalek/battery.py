import os.path
import time
import threading

# capacity  device  power  powers  present  scope  status  subsystem  type  uevent


def get_battery_status(address="00:21:4f:19:34:c2"):

    # we have two controllers so test for them

    capacity = '/sys/class/power_supply/sony_controller_battery_' + address + '/capacity'
    status = '/sys/class/power_supply/sony_controller_battery_' + address + '/status'
    present = '/sys/class/power_supply/sony_controller_battery_' + address + '/present'

    battery_capacity = 0
    battery_status = ""

    with open(capacity) as f:
        battery_capacity = f.read()
    f.close()
    # print("capacity:{}".format(battery_capacity))

    with open(status) as f:
        battery_status = f.read()
    f.close()
    # print("status:{}".format(battery_status))

    with open(present) as f:
        read_data = f.read()
    f.close()
    # print("present:{}".format(read_data))
    return battery_capacity, battery_status


class Battery(threading.Thread):
    def __init__(self)
        super().__init__()
        self.running = False

    def run(self):
        self.running = True


def foo():


if __name__ == "__main__":
    battery_capacity, battery_status = get_battery_status()
    print("capacity:{}status:{}".format(battery_capacity, battery_status))
