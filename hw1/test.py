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
        send_time = time.time()
        sys.stdout.write("%.6f " % (send_time-int(send_time/1000)*1000))
        for host in HOST:
            server_time = serverTime(host)
            sys.stdout.write("%.6f " % (server_time-int(server_time/1000)*1000))
        time.sleep(1)
        print ""

if __name__ == '__main__':
    main()
