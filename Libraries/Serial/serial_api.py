import serial
import time
import re
import custom_logger
import logging
from serial.tools.list_ports import comports
from robot.api.deco import keyword

class serial_api:
    ENTER_CMD = b'\x0d'
    CTRLC_CMD = b'\x03'
    PASSWORD = "root"
    CONF_SERIAL_CMD = "stty -F /dev/ttyHS1 ispeed 115200 ospeed 115200 -parenb -parodd cs8 -hupcl -cstopb cread -clocal -crtscts -ignbrk -brkint -ignpar -parmrk -inpck -istrip -inlcr -igncr -icrnl -ixon -ixoff -iuclc -ixany -imaxbel -iutf8 -opost -olcuc -ocrnl -onlcr -onocr -onlret -ofill -ofdel nl0 cr0 tab0 bs0 vt0 ff0 -isig -icanon -iexten -echo -echoe -echok -echonl -noflsh -xcase -tostop -echoprt -echo"
    SERIAL_PORT_BAUD = 115200

    # Demo clients
    DEMO_HEALTH_DATA = "/usr/bin/inc-demo_healthdata_client"
    DEMO_IO_ENVIRONMENT_SOMEIP = "/usr/bin/inc-demo_io_environment_SomeIp"
    DEMOS=["/usr/bin/inc-demo_healthdata_client", "/usr/bin/inc-demo_io_environment_SomeIp -a", "/usr/bin/inc-demo_io_testing", "/usr/bin/inc-demo_sysinfo_client", "/usr/bin/inc-demo_nvm_client -b"]
    NSM=["/usr/bin/nsm_control --requestRestart=2", "/usr/bin/nsm_control --requestRestart=3", "/usr/bin/nsm_control --requestRestart=7"]
    SYSTEM=["/bin/systemctl is-active flashing.target", "/bin/systemctl is-active application.target", "/bin/systemctl is-active application.target"]
    DEMO_STRESS_START=["/usr/bin/inc-demo_test_client -c 1 -f 1 -g 255 -m 122 -p 1000 -a", "/usr/bin/inc-demo_test_client -c 17 -f 214 -g 255 -m 122 -p 1000 -a",
                       "/usr/bin/inc-demo_test_client -c 17 -f 215 -g 255 -m 11 -p 1000 -a", "/usr/bin/inc-demo_test_client -c 17 -f 217 -g 255 -m 19 -p 1000 -a",
                       "/usr/bin/inc-demo_test_client -c 9 -f 211 -g 0 -m 3 -p 1000 -a", "/usr/bin/inc-demo_test_client -c 9 -f 211 -g 1 -m 3 -p 1000 -a",
                       "/usr/bin/inc-demo_test_client -c 9 -f 213 -g 0 -m 3 -p 1000 -a", "/usr/bin/inc-demo_test_client -c 9 -f 213 -g 1 -m 3 -p 1000 -a",
                       "/usr/bin/inc-demo_test_client -c 18 -f 218 -g 255 -m 122 -p 1000 -a"]  
    DEMO_STRESS_STOP=["/usr/bin/inc-demo_test_client -c 1 -f 1 -g 255 -b", "/usr/bin/inc-demo_test_client -c 17 -f 214 -g 255 -b", "/usr/bin/inc-demo_test_client -c 17 -f 215 -g 255 -b", 
                      "/usr/bin/inc-demo_test_client -c 17 -f 217 -g 255 -b", "/usr/bin/inc-demo_test_client -c 9 -f 211 -g 0 -b", "/usr/bin/inc-demo_test_client -c 9 -f 211 -g 1 -b",
                      "/usr/bin/inc-demo_test_client -c 9 -f 213 -g 0 -b", "/usr/bin/inc-demo_test_client -c 9 -f 213 -g 1 -b", "/usr/bin/inc-demo_test_client -c 18 -f 218 -g 255 -b"]

    DEVCODING = "devcoding --caf 0x0000945e,/usr/share/sysfunc/coding/cafd_mgu_02_a.bin write {} {}"

    def __init__(self):
        self.__log            = logging.getLogger(__class__.__name__)
        self.isSerialOpen     = False
        self.available_ports  = []
        self.ser              = None
        self.__log.info('Target connection setup')

    def __del__(self):
        return

    def serial_port_init(self, port_name = None, port_baud = SERIAL_PORT_BAUD):
            
        if port_name is None:
            try:
                for port in serial.tools.list_ports.comports():
                    self.available_ports.append(port.device)
                    self.available_ports.sort()
                port_name = str(self.available_ports[3])
            except:
                self.__log.error("No ports available!")
                raise serial.SerialException

        try:
            self.ser = serial.Serial(port_name, port_baud)
            self.__log.info("Connected to port %s" % str(port_name))
            self.ser.timeout = 0
            self.ser.write(self.ENTER_CMD)
            time.sleep(0.2)
        except:
            self.__log.error("Serial port {} does not exist or unknown error while trying to open it!".format(port_name))
            raise serial.SerialException
    
    def serial_logging(self):
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
                    self.__log.info("Logged in")
                    self.ser.write(self.ENTER_CMD)
                    time.sleep(0.2)

                    self.__log.info("Configuring target serial port interface")
                    #self.ser.write(self.CONF_SERIAL_CMD.encode())
                    self.ser.write(self.ENTER_CMD)
                    time.sleep(0.2)

                    self.__log.info("Serial connection initialized")
                    self.isSerialOpen = True

                    return

        self.__log.error("Serial port initialization timed out!")
        raise serial.SerialException
    
    def send_to_serial(self, payload, sleep = 0.1):     
        if self.ser.is_open and self.isSerialOpen:
            self.ser.write(self.ENTER_CMD)
            self.ser.write(payload.encode("utf-8"))
            self.ser.write(self.ENTER_CMD)
            time.sleep(sleep)
            self.__log.info(f"Sent to serial: {payload}")
        else:
            self.__log.error("Serial port not open or not correctly initialized!")
            raise serial.SerialException

    def soc_init_sequence(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
        
        tic = toc = time.process_time()

        while 1:
            toc = time.process_time()

            line = self.ser.readline().replace(b"\r\n",b"")
            line = line.decode('utf-8', errors='ignore')      

            if (line.find("DWC_ETH_QOS: Phy detected at ID/ADDR 8") != -1):
                return True
            elif (line.find("login:") != -1):
                return False
            elif toc - tic > 30:
                return 10

    def close_connection(self):
        self.ser.close()

    def success_check(self, message):
        a=0
        while a<30:
            line = self.ser.readline().replace(b"\r\n",b"")
            line = line.decode("utf-8", errors="ignore")
            if line.find(message)!=-1:
                print("found")
                return True
            a=a+1
        raise Exception("error!")


    def check_burst_client(self):
        calls=[0,0,0,0]
        a=0  
        tic = toc = time.process_time()
        while 1:
            toc = time.process_time()
            line = self.ser.readline().replace(b"\r\n",b"")
            line = line.decode("utf-8", errors="ignore")
            if line.find("Total")!=-1:
                requests=([int(s) for s in re.findall(r'-?\d+\.?\d*', line)])
                calls[a]=requests[0]
                a=a+1
                print(requests[0])
                if a==4:
                    if calls[3]<calls[0] and calls[3]<calls[1] and calls[3]<calls[2]:
                        return True
                    else:
                        raise Exception("priorities not respected")
            elif toc - tic > 10:
                self.__log.error("Operation timed out!")
                raise serial.SerialException

    def check_someip(self, data, valid):
        tic = toc = time.process_time()
        while 1:
            toc = time.process_time()
            line = self.ser.readline().replace(b"\r\n",b"")
            line = line.decode("utf-8", errors="ignore")
            if line.find(data)!=-1 and line.find(valid)!=-1:
                return True
            elif toc - tic > 10:
                raise Exception(f"not valid {data}")
        self.close_connection()

    def check_hw_versions(self, hv, hs):
        data = [None, None]
        tic = toc = time.process_time()

        while True:
            toc = time.process_time()
            line = self.ser.readline().replace(b'\r\n',b'')
            line = line.decode('utf-8', errors="ignore")
            if line.find(hv) != -1:
                data[0]=True
            elif line.find(hs) != -1:
                data[1]=True
            elif data[0]==True and data[1]==True:
                return True
            elif toc - tic > 20:
                self.ser.close()
                raise Exception('Operation timed out')

    def devcoding(self, parameter, value):
        self.serial_logging()
        self.__log.info("Sending ")
        self.send_to_serial(self.DEVCODING.format(parameter, value))
