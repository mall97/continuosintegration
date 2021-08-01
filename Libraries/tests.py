from Serial.serial_api import serial_api
from Restart_Rack import restart
import argparse
import time

parser = argparse.ArgumentParser(description='Scripts for testing')
parser.add_argument('--opt', help="1 -> SomeIp, 2 -> BurnClient, 3 -> CanClient, 4 -> DemoStress")
parser.add_argument('--cyl', help="Number of cycles")
parser.add_argument('--port', help="Serial Port")
args = parser.parse_args()



def main():
    
    stress=serial_api()
    arg = int(args.opt)
    cyl = int(args.cyl)
    port = args.port

    if arg == 1:
        for x in range(1,cyl+1):   
            print("CICLO: ",x)
            stress.some_ip(port)
    
    elif arg == 2:    
        for x in range(1,cyl+1):
            print('Cycle number ',x)
            stress.burn_client(port)
    
    elif arg == 3:
        stress.can_client(cyl, port)
    
    elif arg == 4:
        stress.com_stressTest(cyl, port)
    
    elif arg == 5:
        stress.serial_port_init(port_name=port)
        for c in range(1, cyl+1):
            print(f"Devcoding test cycle n. {c}")
            stress.devcoding("CLUSTER_CAF_VERSION_MINOR", 2)
            time.sleep(10)
            for i in range(1,6):
                print(f'Restart {i}')
                restart.res_rack("COM34")
                print('Sleeping 30 seconds')
                time.sleep(30)
            
        print(f"Finished devcoding test of {cyl} cicles.")
                
    else:
        print("Wrong option")


if __name__ == "__main__":
    main()
