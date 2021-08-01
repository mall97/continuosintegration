from argparse import ArgumentParser
import time 
import os
import sys
import fileinput

class dlt_local_windows():
    def replace(self, file, searchExp, replaceExp):
        for line in fileinput.input(file, inplace=1):
            if searchExp in line:
                #line = line.replace(replaceExp)
                sys.stdout.write(replaceExp)
            else:
                sys.stdout.write(line)
    
    
    def create_logs(self, log_name, target):
        
        if target=="IDC":
                ip="        <hostname>169.254.53.255</hostname>\n"
                
        else:
                ip="        <hostname>169.254.125.242</hostname>\n"
        
        self.__projectfile=      'Libraries\\dlt_viewer\\config\\DLTconfig.dlp'
        self.__executable=       'C:\\Users\\MGU22\\Desktop\\DltViewer\\dlt_viewer.exe'
        self.__file=             f'Libraries\\dlt_viewer\\logs\\{log_name}.dlt'

        self.replace(self.__projectfile, "<hostname>", ip)

        try:
            if os.path.exists(self.__file):
                os.remove(self.__file)

            self.__f = open(self.__file, "a+")
            self.__f.close()
            self.__cmd = 'start "dlt viewer" "{exe}" -l "{logs}" -p "{prjfile}"'.format(exe=self.__executable, logs=self.__file, prjfile=self.__projectfile)
            print("cmd = " + self.__cmd)
            os.system(self.__cmd)
            time.sleep(30)
        except Exception as e:
            print(str(e))

    def kill_dlt(self):
        os.system('taskkill /T /F /IM dlt_viewer.exe')

    def read_dlt(self, newlog, data):
        self.__f=open(f'Libraries\\dlt_viewer\\logs\\{newlog}.dlt', 'r', encoding="utf8", errors='ignore')
        for line in self.__f.readlines():
            if(line.find(data)!=-1):
                print(data)
                self.__f.close()
                return True
        self.__f.close()
        raise Exception('error in ->'+data)