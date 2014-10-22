# hw1.py -- CS 271 Assn. 1

import socket, sys, time 

HOST = [ '54.169.67.45', '54.207.15.207', '54.191.73.92' ]
PORT = 5000

SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def serverTime(host):
    SOCK.sendto("\n", (host, PORT))
    return float(SOCK.recv(4096))

def main():
    while True:
        sys.stdout.write("%.6f " % (time.time()))
        for host in HOST:
            sys.stdout.write("%.6f " % (serverTime(host)))
        sys.stdout.write("%.6f\n" % (time.time()))
        time.sleep(1)


if __name__ == '__main__':
    main()
