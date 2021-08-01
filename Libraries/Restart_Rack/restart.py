import sys, pathlib

sys.path.insert(1, str(pathlib.Path(__file__).parent.absolute()))

from TesterlyzerIBox4 import TesterlyzerIBox4
import time

def tes_rack():
    port=sys.argv[1]
    psu = TesterlyzerIBox4(port)
    for x in range(0,30):
        psu.powersupply_set_voltage(0)
        time.sleep(10)
        psu.powersupply_set_voltage(1)
        print(x,"Restart")
        time.sleep(130)

def res_rack(port):
    psu = TesterlyzerIBox4(port)
    psu.powersupply_set_voltage(0)
    time.sleep(45)
    psu.powersupply_set_voltage(1)
    print("Restart")
    time.sleep(10)

def current():
    port=sys.argv[1]
    psu = TesterlyzerIBox4(port)
    value=psu.powersupply_get_current()
    print(value)


def power_off():
    port=sys.argv[1]
    psu = TesterlyzerIBox4(port)
    psu.powersupply_set_voltage(0)    

if __name__ == "__main__":
    res_rack(sys.argv[1])


#PowerOff()
#Current()