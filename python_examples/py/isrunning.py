#!/usr/bin/env python2.7
import os
def write_pidfile_or_die(path_to_pidfile):

    if os.path.exists(path_to_pidfile):
        pid = int(open(path_to_pidfile).read())

    if pid_is_running(pid):
        print("Sorry, found a pidfile!  Process {0} is still running.".format(pid))
        raise SystemExit

    else:
        os.remove(path_to_pidfile)

    open(path_to_pidfile, 'w').write(str(os.getpid()))
    return path_to_pidfile

write_pidfile_or_die('/tmp/test.pid')
