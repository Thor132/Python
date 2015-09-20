import signal
import subprocess
import sys
import time

trackedProcesses = []

class TrackedProcess(object):
    def __init__(self, processArgs):
        self.processArgs = processArgs
        self.process = None
        self.Start()
    def GetPID(self):
        if self.process:
            return self.process.pid
        else:
            return 0
    def Start(self):
        self.process = subprocess.Popen(processArgs)
        print "Started process pid:{0}".format(self.process.pid)
    def IsRunning(self):
        return self.process != None and self.process.poll() == None
    def Kill(self):
        if self.IsRunning():
            self.process.kill()
            print "Killed process pid {0}".format(self.process.pid)

def signal_handler(signal, frame):
    print "Killing launched processes"
    for process in trackedProcesses:
        if process.IsRunning():
             process.Kill()
        else:
            print "Process pid {0} has already exited".format(process.GetPID())
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    assert len(sys.argv) > 2
    numtrackedProcesses = int(sys.argv[1])
    processArgs = sys.argv[2:]
    print "Starting {0} process using the command line '{1}'".format(numtrackedProcesses, " ".join(processArgs))
    
    while(len(trackedProcesses) < numtrackedProcesses):
        process = TrackedProcess(processArgs)
        trackedProcesses.append(process)
    
    while True:
        for process in trackedProcesses:
            if not process.IsRunning():
                print "Process pid {0} has exited - restarting".format(process.GetPID())
                process.Start()
                break
        time.sleep(5)