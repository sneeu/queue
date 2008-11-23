#!/usr/bin/env python
import os
import sys

import queue


LOGFILE = '/var/log/pyqueue.log'
PIDFILE = '/var/run/pyqueue.pid'
UID = 501
GID = 20
USERPROG = queue.start_server


class Log:
    def __init__(self, f):
        self.f = f

    def write(self, s):
        self.f.write(s)
        self.f.flush()


def main():
    #os.chdir('/root/data')
    sys.stdout = sys.stderr = Log(open(LOGFILE, 'a+'))
    os.setegid(GID)
    os.seteuid(UID)
    USERPROG()


if __name__ == '__main__':
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        sys.stderr.write('fork #1 failed: %d (%s)' % (e.errno, e.strerror))
        sys.exit(1)

    os.chdir('/')
    os.setsid()
    os.umask(0)

    try:
        pid = os.fork()
        if pid > 0:
            open(PIDFILE, 'w').write("%d" % pid)
            sys.exit(0)
    except OSError, e:
        sys.stderr.write('fork #2 failed: %d (%s)' % (e.errno, e.strerror))
        sys.exit(1)

    main()
