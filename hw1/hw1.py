# hw1.py -- CS 271 Assn. 1

import socket, sys, time 
from operator import attrgetter, itemgetter

HOST = [ '54.169.67.45', '54.207.15.207', '54.191.73.92' ]
PORT = 5000

class TimeServerResp:
    def __init__(self, t, rtt, sent):
        self.t = t    # times reported by server
        self.rtt = rtt   # round trip time
        self.sent = sent # physical clock time of request

    def time(self):
        return time.time()-(self.sent+0.5*self.rtt)+self.t

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
        self.skew = minResp.t - minResp.sent - 0.5*minResp.rtt

    def syncMarzullo(self, resp):
        # populate list of tuples
        windows = []
        for r in resp:
            windows.append((r.time()-0.5*r.rtt, -1))
            windows.append((r.time()+0.5*r.rtt, +1))

        # sort listof tuples
        windows.sort(key=itemgetter(1))

        # initialize best, cnt
        best, cnt = 0, 0

        # loop in ascending order
        for i in range(len(tup)):
            cnt = cnt - windows[i][1]
            if cnt > best:
                best = cnt
                beststart = windows[i][0]
                bestend = windows[i+1][0]

        self.skew = minResp.t - minResp.sent - 0.5*minResp.rtt
        


    def time(self):
        return time.time() + self.skew

def main():
    clock = Clock()
    servers = [TimeServer(host) for host in HOST]

    while True:
        resp = [s.query() for s in servers]
        current_time = clock.time()
        #clock.syncMinRTT(resp)
        clock.syncMarzullo(resp)
        server_time = [r.time() for r in resp]
        updated_time = clock.time()
        delta = updated_time - current_time
        sys.stdout.write("%f " % (current_time-int(current_time/1000)*1000))
        for t in server_time:
            sys.stdout.write("%f " % (t-int(t/1000)*1000))
        sys.stdout.write("%f " % (updated_time-int(updated_time/1000)*1000))
        sys.stdout.write("%f\n" % (clock.skew))

        time.sleep(2)


if __name__ == '__main__':
    main()
