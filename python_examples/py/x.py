        # Inform start/stop script that all is well
        if os.path.isfile(MONITOR_STARTUP_FILE):
            os.unlink(MONITOR_STARTUP_FILE)        

        # Check if already running...
        pid = str(os.getpid())
        self.pidfile = "/tmp/Monitor.pid"
        if os.path.isfile(pidfile):
            print "%s already exists, exiting" % pidfile
            sys.exit()
        else:
            file(pidfile, 'w').write(pid)


        self.t = threading.Thread(target=self.mainLoop)
        self.t.setDaemon(False)
        self.t.start()
        return self.t

     def stop(self):
        os.unlink(pidfile)
################################################################################
# SIGINT HANDLER CODE                                                          #
################################################################################
stopflag     = False
def mon_sig_handler(signum, frame):
    if signum == signal.SIGINT:
        global stopflag
        stopflag = True
    return
