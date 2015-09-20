import signal
import subprocess
import sys
import time

trackingProcesses = []
def StartProcess(processArgs):
    process = subprocess.Popen(processArgs)
    print "Started process pid:{0}".format(process.pid)
    return process

def signal_handler(signal, frame):
    print "Exiting launched processes"
    for process in trackingProcesses:
        if process.poll() == None:
             print "Killing process pid:{0}".format(process.pid)
             process.kill()
        else:
            print "Process pid:{0} was already exited".format(process.pid)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    assert len(sys.argv) > 2
    numtrackingProcesses = int(sys.argv[1])
    processArgs = sys.argv[2:]
    print "Starting {0} process using '{1}'".format(numtrackingProcesses, " ".join(processArgs))
	
    while(len(trackingProcesses) < numtrackingProcesses):
        process = StartProcess(processArgs)
        trackingProcesses.append(process)
	
    while True:
        for process in trackingProcesses:
            if process.poll() != None:
                print "Process pid:{0} has exited  - restarting".format(process.pid)
                trackingProcesses.remove(process)
                trackingProcesses.append(StartProcess(processArgs))
                break
        time.sleep(5)