# hw1.py -- CS 271 Assn. 1

import socket, sys, time 
from operator import attrgetter

HOST = [ '54.169.67.45', '54.207.15.207', '54.191.73.92' ]
PORT = 5000

class TimeServerResp:
    def __init__(self, t, rtt, sent):
        self.time = t    # times reported by server
        self.rtt = rtt   # round trip time
        self.sent = sent # physical clock time of request

    def time(self):
        return time.time()-(self.sent+self.rtt)+self.time

class TimeServer:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, host):
        self.host = host

    def query(self):
        send_time = time.time()
        TimeServer.sock.sendto("\n", (self.host, PORT))
        server_time = TimeServer.sock.recv(4096)
        recv_time = time.time()
        return TimeServerResp(float(server_time), recv_time-send_time, send_time)


class Clock:
    def __init__(self):
        self.skew = 0.0

    def syncMinRTT(self, resp):
        minResp = min(resp, key=attrgetter('rtt'))
        self.skew = minResp.time - minResp.sent - 0.5*minResp.rtt

    def syncMarzullo(self, resp):
        resp.sort(key=attrgetter('rtt'))

    def time(self):
        return time.time() + self.skew

def main():
    clock = Clock()
    servers = [TimeServer(host) for host in HOST]

    while True:
        resp = [s.query() for s in servers]
        current_time = clock.time()
        clock.syncMinRTT(resp)
        #clock.syncMarzullo(resp)
        for i in resp: print type(i.time())
        server_time = [r.time() for r in resp]
        updated_time = clock.time()
        sys.stdout.write("%f " % (current_time))
        for t in server_time:
            sys.stdout.write("%f " % (t))
        sys.stdout.write("%f " % (updated_time))

        time.sleep(2)


if __name__ == '__main__':
    main()
