import os
import subprocess

class on_off_vcar():
    def kill_vcar(self):
        f = open("C:\\Users\\MGU22\\Desktop\\jenkins\\workspace\\Regression_OSIS\\my_pid.txt", "r")
        PID=f.read()
        __cmd = f'taskkill /F /PID {PID}'
        os.system(__cmd)
    
    def run_vcar(self):
        subprocess.Popen(["python", "C:\\Users\\MGU22\\Desktop\\jenkins\\workspace\\Regression_OSIS\\Libraries\\vcar\\vcar.py"], creationflags=subprocess.DETACHED_PROCESS)
