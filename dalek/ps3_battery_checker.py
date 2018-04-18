if __name__ == "__main__":
    '''
    This if statement is needed for testing, to locate the modules needed
    if we are running the file directly.
    '''
    import sys
    from os import path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import os.path
import time
import threading
from dalek import debug
from termcolor import colored

# capacity  device  power  powers  present  scope  status  subsystem  type  uevent


def init():
    # you may have more than one device so add them to the list
    # It will only use the first device it finds so if two or more devices are in
    # the list, and connected, it may not find the right one
    address_list = ['00:21:4f:19:34:22', '00:21:4f:19:34:c2']
    address = "Not Connected"
    for add in address_list:
        folder = '/sys/class/power_supply/sony_controller_battery_' + add
        if os.path.exists(folder):
            debug.print_to_all_devices(
                colored("\nController Connected:{}\n".format(add), 'green'), "BL")
            address = add

    return address


def get_battery_status(address="00:21:4f:19:34:c2"):

    folder = '/sys/class/power_supply/sony_controller_battery_' + address

    capacity = '/sys/class/power_supply/sony_controller_battery_' + address + '/capacity'
    status = '/sys/class/power_supply/sony_controller_battery_' + address + '/status'
    present = '/sys/class/power_supply/sony_controller_battery_' + address + '/present'

    battery_capacity = 0
    battery_status = "Not Connected"

    # print(os.path.exists(folder))
    if os.path.exists(folder):
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


class StatusMonitor(threading.Thread):

    battery_capacity = 0
    battery_status = "Not Connected"
    threshold = 25

    def __init__(self, frequency=60):
        super().__init__()
        self.running = False
        self.frequency = frequency

    def stop_running(self):
        self.running = False

    def run(self):
        self.running = True
        self.address = init()
        while self.address == "Not Connected":
            self.address = init()
            debug.print_to_all_devices(
                colored("NO Controller Connected", 'red'), "BL")
            time.sleep(1)

        while self.running:
            self.battery_capacity, self.battery_status = get_battery_status(
                self.address)

            if self.battery_status == "Not Connected":
                debug.print_to_all_devices(
                    colored("NO Controller Connected", 'red'), "BL")
            else:

                if int(self.battery_capacity) < 25:
                    debug.print_to_all_devices(colored("Controller Battery LOW --- RECHARGE IT \n---capacity:{}---status:{}".format(
                        self.battery_capacity, self.battery_status), 'red'), "BL")

                elif int(self.battery_capacity) <= 51:
                    debug.print_to_all_devices(colored("Controller Battery -- LESS THAN HALF FULL \n---capacity:{}---status:{}".format(
                        self.battery_capacity, self.battery_status), 'yellow'), "BM")
                else:
                    debug.print_to_all_devices(colored("Controller Battery -- GOOD \n---capacity:{}---status:{}".format(
                        self.battery_capacity, self.battery_status), 'green'), "BG")
            # create a timer that can be stopped immediately
            for x in range(self.frequency):
                time.sleep(1)
                if self.running == False:
                    break


def main():
    # just for testing things work
    debug.turn_debug_on()
    battery = StatusMonitor(2)
    battery.start()
    time.sleep(3)
    battery.stop_running()

    battery.join() 


if __name__ == "__main__":
    main()
