import time 
import os

class diagnoser():
    def run_diagnoser(self, script, dtc, target):
        try:
            if os.path.exists(dtc):
                os.remove(dtc+".txt")

            if target=="IDC":
                ip="169.254.53.255"
            else:
                ip="169.254.125.242"

            self.__cmd = f'start "DiagnoserRCP" "C:\\Users\\MGU22\\Desktop\\Diagnoser_v.3.1.0.8\\runtime.exe" -script:"Libraries\\Diagnoser\\{script}.skr" -scriptreport:"{dtc}.txt" -defaulttarget:63 -defaultsource:F1 -connectionDevice:"ETHERNET (6B Header)" -connectionDeviceSettings:{ip}:6801'
            os.system(self.__cmd)
        except Exception as e:
            print(str(e))

    def check_diagnoser(self, dtc):
        self.__f=open(f'{dtc}.txt', 'r', encoding="utf8", errors='ignore')
        for line in self.__f.readlines():
            if(line=='Reason: Negative Response\n'):
                self.__f.close()
                raise Exception('wrong DTC\DTCs')
        self.__f.close()
        return True

    def check_diagnoser_2(self, dtc, data):
        self.__f=open(f'{dtc}.txt', 'r', encoding="utf8", errors='ignore')
        for my_line in self.__f.readlines():
            if my_line.find("Received: "+data)!=-1:
                self.__f.close()
                return True 
        self.__f.close()
        raise Exception(data)

    def check_dtc_error(self, dtc, data):
        self.__f=open(f'{dtc}.txt', 'r', encoding="utf8", errors='ignore')
        for my_line in self.__f.readlines():
            if my_line.find(data)!=-1:
                self.__f.close()
                raise Exception(data)
        self.__f.close()
        return True

    def check_equal_number_of_bytes(self, dtc, data, bytes):
        self.__f=open(f'{dtc}.txt', 'r', encoding="utf8", errors='ignore')
        for my_line in self.__f.readlines():
            if my_line.find(data)!=-1:
                number_bytes=my_line.split(',')
                if len(number_bytes)!=int(bytes):
                    self.__f.close()
                    raise Exception("incorrect number of bytes")
        return True
        self.__f.close()
        raise Exception("Wrong answer from Diagnoser")


    def check_equal_or_bigger_number_of_bytes(self, dtc, data, bytes):
        self.__f=open(f'{dtc}.txt', 'r', encoding="utf8", errors='ignore')
        for my_line in self.__f.readlines():
            if my_line.find(data)!=-1:
                number_bytes=my_line.split(',')
                if len(number_bytes)>=int(bytes):
                    self.__f.close()
                    return True
                else:
                    self.__f.close()
                    raise Exception("incorrect number of bytes")
        self.__f.close()
        raise Exception("Wrong answer from Diagnoser")
    
    def write_diag_skr(self, jobs, result):
        f = open("Libraries\\Diagnoser\\generic.skr", "w")
        f.write(f"DIAG [DIAG test]          SEND [{jobs}]                        	EXPECT [{result}] 				  TIMEOUT [5000]")
        f.close()