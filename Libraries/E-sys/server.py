import os
import time
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Start or stop E-sys server')
parser.add_argument('--opt', help="1 -> start server, 2 -> stop server")
args = parser.parse_args()

ESYS_PATH = "C:\\EC-Apps\\ESG\\E-Sys\\E-Sys.bat"

def start_server():
    process=subprocess.Popen([ESYS_PATH, "-startserver"], creationflags=subprocess.DETACHED_PROCESS)
    time.sleep(20)
    print("Server On")

def stop_server():
    cmd = f"{ESYS_PATH} -server -stop"
    os.system(cmd)
    print("Server Off")

if __name__ == '__main__':
    if int(args.opt)==1:
        start_server()
    else:
        stop_server()