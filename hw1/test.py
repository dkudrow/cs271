# hw1.py -- CS 271 Assn. 1

import socket, sys, time 

SERVERS = [ ('54.169.67.45', 5000),
                ('54.207.15.207', 5000),
                ('54.191.73.92', 5000),
                ('54.172.168.244', 5000),
                ('128.111.44.106', 12291) ]

SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def serverTime(server):
    SOCK.sendto("\n", server)
    return float(SOCK.recv(4096))

def main():
    while True:
        send_time = time.time()
        sys.stdout.write("%.6f " % (send_time-int(send_time/1000)*1000))
        for s in SERVERS:
            server_time = serverTime(s)
            sys.stdout.write("%.6f " % (server_time-int(server_time/1000)*1000))
        time.sleep(1)
        print ""

if __name__ == '__main__':
    main()
