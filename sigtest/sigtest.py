#!/usr/bin/env python3
# vim modeline (put ":set modeline" into your ~/.vimrc)
# vim:set expandtab ts=4 sw=4 ai ft=python:

import time
import signal

# just the ones we can catch
sigs = {
    1: "SigHUP",
    2: "SigINT",
    3: "SigQUIT", # nginx likes this for graceful shutdown
    4: "SigILL",
    6: "SigABRT",
    8: "SigFPE",
    11: "SigSEGV",
    13: "SigPIPE",
    14: "SigALRM",
    15: "SigTERM",
    20: "SigWINCH", # apache uses this 'window change' signal for a graceful shutdown
    28: "SigWINCH" # may also be # 28
}

def main():
    def sighandle(signum, frame):
        print("Signal {} ({}) received".format(sigs[signum], signum))

    for signum in sigs:
        print("Binding signal handler for {} ({})".format(sigs[signum], signum))
        signal.signal(signum, sighandle)

    while True:
        print(time.time())
        time.sleep(1)
#        signal.pause() # wait until we are told to quit

if __name__ == "__main__":
    main()
