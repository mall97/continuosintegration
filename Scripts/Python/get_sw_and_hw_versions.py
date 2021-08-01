import serial
import argparse
import time

class VersionFactory():

    ENTER_CMD = b'\x0d'
    CTRLC_CMD = b'\x03'
    PASSWORD = "root"
    SERIAL_PORT_BAUD = 115200

    def __init__(self,port):
        self.isSerialOpen     = False
        self.available_ports  = []
        self.ser              = None
        self.port_name=port

    def __serial_port_init(self,port_baud = SERIAL_PORT_BAUD):
            try:
                self.ser = serial.Serial(self.port_name, port_baud)
                self.ser.timeout = 0
                self.ser.write(self.ENTER_CMD)
                time.sleep(0.2)
            except:
                raise serial.SerialException
        
    def __serial_logging(self):
        tic = toc = time.process_time()

        while toc - tic < 20:
            toc = time.process_time()

            size = self.ser.inWaiting()

            if size:
                data = self.ser.read(size)
                strData = data.decode("utf-8")
                self.ser.write(self.ENTER_CMD)
                time.sleep(2)
                
                if strData.find("login:") != -1:
                    self.ser.write(self.PASSWORD.encode())
                    self.ser.write(self.ENTER_CMD)
                    time.sleep(0.2)

                if strData.find("root@mgu22") != -1 or strData.find("~ #") != -1:
                    self.ser.write(self.ENTER_CMD)
                    time.sleep(0.2)

                    self.ser.write(self.ENTER_CMD)
                    time.sleep(0.2)

                    self.isSerialOpen = True

                    return

        raise serial.SerialException
        
    def __send_to_serial(self, payload, sleep = 0.1):     
        if self.ser.is_open and self.isSerialOpen:
            self.ser.write(self.ENTER_CMD)
            self.ser.write(payload.encode("utf-8"))
            self.ser.write(self.ENTER_CMD)
            #print(f"Sent to serial: ${payload}")
            time.sleep(sleep)
        else:
            raise serial.SerialException
    
    def get_sw_and_hw_versions(self):
        self.__serial_port_init()
        self.__serial_logging()
        
        
        self.__send_to_serial('cat /etc/os-release',1)

        soc_version = None
        ioc_version = None
        hw_version = None
        hw_sample = None
        data = [None, None, None, None]

        import re
        
        tic = toc = time.process_time()

        while True:
            toc = time.process_time()
            line = self.ser.readline().replace(b'\r\n',b'')
            line = line.decode('utf-8', errors="ignore")
            #print(line)
            if not soc_version and line.find("VERSION") != -1:
                soc_version = re.findall(r'"(.*?)"', line)[0]
                break
            elif toc - tic > 20:
                self.ser.close()
                raise Exception('Operation timed out')
            
        self.__send_to_serial('inc-demo_io_testing -t 1',1)



        tic = toc = time.process_time()

        while True:
            toc = time.process_time()
            line = self.ser.readline().replace(b'\r\n',b'')
            line = line.decode('utf-8', errors="ignore")
            #print(line)
            if hw_version is None and line.find("HardwareVariant") != -1:
                hw_version = " ".join(line.split(" ")[7:9])
            elif hw_sample is None and line.find("HardwareSample") != -1:
                hw_sample = line.split(" ")[-1]
            elif ioc_version is None and line.find("SoftwareVersion") != -1:
                ioc_version = line.split(" ")[-1]
                break
            elif toc - tic > 20:
                self.ser.close()
                raise Exception('Operation timed out')


        self.ser.close()
        data[0] = soc_version
        data[1] = ioc_version
        data[2] = hw_version
        data[3] = hw_sample
        return data


if __name__ == "__main__":

    

    parser = argparse.ArgumentParser(description= 'Get SW and HW versions from Target')
    parser.add_argument('-p','--port', help='Serial Port that the target is connected')

    args = parser.parse_args()

    ver_factory = VersionFactory(args.port)
    versions = ver_factory.get_sw_and_hw_versions()
    if all(versions):
        print(f"SOC: {versions[0]}, IOC: {versions[1]}, HW: {versions[2]} {versions[3]}")
    