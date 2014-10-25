# hw1.py -- CS 271 HW #1
#
# Author: Daniel Kudrow
# Due: Oct. 24 2014

import socket, sys, time 
from operator import attrgetter

SERVERS = [ ('54.169.67.45', 5000),
                ('54.207.15.207', 5000),
                ('54.191.73.92', 5000),
                ('54.172.168.244', 5000),
                ('128.111.44.106', 12291) ]

######################################################################
# This class wraps the timeserver's response. It also approximates the
# timeserver's current time.
#
class TimeServerResp:
    # construct a server response
    def __init__(self, t, rtt, sent):
        self.t = t       # server timestamp
        self.rtt = rtt   # round trip time
        self.sent = sent # local physical clock time of request

    # return current time on server
    def time(self):
        return time.time()-(self.sent+0.5*self.rtt)+self.t
#
######################################################################

######################################################################
# This class wraps a hostname and port tuple that can be queried for a Unix
# timestamp.
#
class TimeServer:
    # all queries share a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # construct a TimeServer
    def __init__(self, host):
        self.host = host # tuple of (host, port)

    # request a TimeServerResp from this instance's timesever
    def query(self):
        send_time = time.time()
        TimeServer.sock.sendto("\n", self.host)
        server_time = TimeServer.sock.recv(4096)
        recv_time = time.time()
        return TimeServerResp(float(server_time), recv_time-send_time, send_time)
#
######################################################################

######################################################################
# This class acts as a virtual clock. All it really does is keep track of a
# 'skew' which can be added to the physical clock to create virtual time.
# The syncXXX methods can be used to synchronize the clock using a list of
# timeserver responses.
#
class Clock:
    # construct a new clock -- it starts as a copy of the physical clock
    def __init__(self, drift=15):
        self.skew = 0.0
        self.drift = drift

    # determine necessary synv interval to keep drift < delta ms/min
    def interval(self, delta=1):
        return 60.0 * delta / (self.drift * 2)

    # synchronize the clock to the closest time server (lowest RTT)
    def syncMinRTT(self, resp):
        minResp = min(resp, key=attrgetter('rtt'))
        self.skew = minResp.t - minResp.sent - 0.5*minResp.rtt

    # synchronize the clock using all time servers
    def syncMarzullo(self, resp):
        # populate list of tuples
        currentTime = time.time()
        windows = []
        for r in resp:
            t = r.time()
            windows.append((t-0.5*r.rtt, -1))
            windows.append((t+0.5*r.rtt, +1))

        # sort listof tuples
        windows.sort()

        # initialize best, cnt
        best, cnt = 0, 0

        # loop in ascending order
        for i in range(len(windows)):
            cnt = cnt - windows[i][1]
            if cnt > best:
                best = cnt
                beststart = windows[i][0]
                bestend = windows[i+1][0]

        self.skew = currentTime - (beststart + 0.5*(bestend-beststart))

    # get the clock's virtual time
    def time(self):
        return time.time() + self.skew
#
######################################################################

# make things look nice for Victor
def format_time(t):
    ret = time.strftime('%H:%M:', time.localtime(t))
    return ret + "%07.4f" % ((t-int(t)/100*100) % 60)

def main():
    # initialize clock and time servers
    clock = Clock()
    servers = [TimeServer(s) for s in SERVERS]

    # set defaults
    resync_interval = clock.interval()
    sync_method = clock.syncMarzullo

    # parse command line args
    argc = len(sys.argv)
    for i in range(1, argc):
        if sys.argv[i] == '-i':
            if (i+1 < argc) and (float(sys.argv[i+1]) > 0):
                resync_interval = float(sys.argv[i+1])
            else:
                print 'WARNING: bad sync interval, default to 2s'
                resync_interval = 2
        elif sys.argv[i] == '-s':
            if (i+1 < argc) and (sys.argv[i+1][0] == 'm'):
                sync_method = clock.syncMarzullo
            elif (i+1 < argc) and (sys.argv[i+1][0] == 'r'):
                sync_method = clock.syncMinRTT
            else:
                print 'WARNING: bad sync method, default to marzullo'
                sync_method = clock.syncMarzullo

    # print parameters
    print "Resyncs per minute to keep drift < 1 ms/min: ", clock.interval()
    print "Resyncs per minute to keep drift < 1 us/min: ", clock.interval(delta=.001)

    # print header
    header = "Curent Time\t"
    for i in range(1, len(SERVERS)+1):
        header += 'Server %d Time\tRTT\t' % (i)
    header += 'Updated Time'
    print header

    # main loop
    while True:
        begin_loop = time.time()
        resp = [s.query() for s in servers]
        current_time = clock.time()
        sync_method(resp)
        server_time = [r.time() for r in resp]
        updated_time = clock.time()
        delta = updated_time - current_time

        # print
        sys.stdout.write("%s\t" % (format_time(current_time)))
        for i in range(len(resp)):
            sys.stdout.write("%s\t%.4f\t" % (format_time(server_time[i]), resp[i].rtt))
        sys.stdout.write("%s\n" % (format_time(updated_time)))

        # only sleep as long as we need to
        sleep_time = resync_interval-(time.time()-begin_loop)
        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == '__main__':
    main()

