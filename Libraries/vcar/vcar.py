#!/usr/bin/env python
#
# Send UDP multicast packets.
# Requires that your OS kernel supports IP multicast.
#
import time
import struct
import socket
import logging
import os


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger()
 
 
MYPORT = 30500
MYGROUP_4 = '239.192.255.1'
MYTTL = 1  # Increase to reach other networks

def writePidFile():
  if os.path.exists('my_pid.txt'):
        os.remove('my_pid.txt')
  pid = str(os.getpid())
  f = open('my_pid.txt', 'w')
  f.write(pid)
  f.close()
 
 
def main():
    technica='160.48.199.121'
    writePidFile()
    sender(MYGROUP_4, technica)
 
def sender(group, technica):

    addrinfo= socket.getaddrinfo(group, None)[0]
 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((technica,0))
    #sock.bind(('169.254.230.177',0))
  
    # Set Time-to-live (optional)
    ttl_bin = struct.pack('@i', MYTTL)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
 
    while True:
        data = b'\x40\x10\x00\x40\x00\x01\x97\x03'
        sock.sendto(data, (addrinfo[4][0], MYPORT))
        logger.info("Keep-alive broadcasted to %s port %d", addrinfo[4][0], MYPORT)
        time.sleep(0.64)
 
if __name__ == '__main__':
    main()