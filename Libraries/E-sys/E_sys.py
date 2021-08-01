import os
import time
import argparse
import fileinput
import sys

parser = argparse.ArgumentParser(description="E-sys Automation")
parser.add_argument("-img", help="name of image directory for example (MGU22_20w48.5-1-15)")
parser.add_argument("-vin", help="vin number (example : 169.254.94.199)")
args = parser.parse_args()
class E_sys:
    def __init__(self):
        self.esys_path = "C:\\EC-Apps\\ESG\\E-Sys\\E-Sys.bat"
        self.image = args.img
        self.vin = args.vin

        if self.vin=="169.254.94.199":
            for item in os.listdir(f"C:\\Users\\MGU22\\Desktop\\images\\{self.image}\\mgu22"):
                if item.find(".pdx") != -1:
                    self.pdx_path = f"C:\\Users\\MGU22\\Desktop\\images\\{self.image}\\mgu22\\{item}"
                elif item.find("svt") != -1:
                    self.svt_path = f"C:/Users/MGU22/Desktop/images/{self.image}/mgu22/{item}"
        elif self.vin=="169.254.125.54":
            for item in os.listdir(f"C:\\Users\\MGU22\\Desktop\\images\\{self.image}"):
                if item.find(".pdx") != -1:    
                    self.pdx_path = f"C:\\Users\\MGU22\\Desktop\\images\\{self.image}\\{item}"
                elif item.find("svk") != -1:
                    self.svt_path = f"C:/Users/MGU22/Desktop/images/{self.image}/{item}"
            
        self.connect = "C:\\Users\\MGU22\\Desktop\\jenkins\\workspace\\Flashing_E-sys\\Libraries\\E-sys\\esys_config.properties"
        self.tal = "C:\\Users\\MGU22\\Desktop\\jenkins\\workspace\\Flashing_E-sys\\Libraries\\E-sys\\tal_config.properties"
        #self.connect = os.path.abspath("esys_config.properties")
        #self.tal = os.path.abspath("tal_config.properties")
        self.generated_tal = "C:\\Data\\TAL\\generatedTal.xml"
        self.__SUCCESS_CODE = 0

    def replace(self, file,searchExp,replaceExp):
        for line in fileinput.input(file, inplace=1):
            if searchExp in line:
                #line = line.replace(replaceExp)
                sys.stdout.write(replaceExp)
            else:
                sys.stdout.write(line)

    def change_pdx(self):
        cmd = f"{self.esys_path} -pdximport {self.pdx_path} -project {self.image}"
        result = os.system(cmd)
        if self.__SUCCESS_CODE != result:
            raise Exception("Error in PDX charger")

    def create_connection(self):
        if self.vin=="169.254.94.199":
            self.replace(self.connect, "PROJECT", f"PROJECT = G070_{self.image}\n")

        elif self.vin=="169.254.125.54":
            self.replace(self.connect, "PROJECT", f"PROJECT = U006_{self.image}\n")

        cmd = f"{self.esys_path} -server -openconnection {self.connect}"
        result = os.system(cmd)
        if self.__SUCCESS_CODE != result:
            raise Exception("Error in connection")
        print("Connected")

    def close_connection(self):
        cmd = f"{self.esys_path} -server -closeconnection"
        result = os.system(cmd)

    def tal_process(self):
        if self.vin=="169.254.94.199":                                                                   #MGU
            self.replace(self.tal, "PROJECT", f"PROJECT = G070_{self.image}\n")   
            self.replace(self.tal, "VEHICLEINFO", "VEHICLEINFO = G070\n")
            self.replace(self.tal, "FA", "FA = C:/Data/FA/FA_G70_MGU22_KRAKOV_HIGH.xml\n")
            self.replace(self.tal, "SVT", f"SVT = {self.svt_path}\n")
            self.replace(self.generated_tal, "<hostname>", "            <hostname>LPT-LE1004</hostname>\n")
            self.replace(self.generated_tal, "<mcdProjectName>", f"            <mcdProjectName>G070_{self.image}</mcdProjectName>\n")  
        
        elif self.vin=="169.254.125.54":                                                                #IDC
            self.replace(self.tal, "PROJECT", f"PROJECT = U006_{self.image}\n")   
            self.replace(self.tal, "VEHICLEINFO", "VEHICLEINFO = U006\n")
            self.replace(self.tal, "FA", "FA = C:/Data/FA/FA_U006.xml\n")
            self.replace(self.tal, "SVT", f"SVT = {self.svt_path}\n") 
            self.replace(self.generated_tal, "<hostname>", "            <hostname>DESKTOP-MGU-CT2</hostname>\n")
            self.replace(self.generated_tal, "<mcdProjectName>", f"            <mcdProjectName>U006_{self.image}</mcdProjectName>\n")  

        self.replace(self.generated_tal, "<accessLink>", f"            <accessLink>EthernetAccessLinkImpl [bus=ETHERNET, ip=/{self.vin}, port=6801]</accessLink>\n")
        cmd = f"{self.esys_path} -talexecution {self.tal}"
        result = os.system(cmd)

if __name__ == '__main__':
    test = E_sys()
    test.change_pdx()
    #test.create_connection()
    test.tal_process()
    #test.close_connection()
